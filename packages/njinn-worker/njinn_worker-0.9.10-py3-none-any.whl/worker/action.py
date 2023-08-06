import configparser
import datetime
import decimal
import importlib
import io
import json
import os
import re
import signal
import sys
import traceback
import uuid
from contextlib import redirect_stderr, redirect_stdout

import requests
from requests_jwt import JWTAuth, payload_path

from api_client import NjinnAPI
from cryptography.fernet import Fernet, InvalidToken


class WorkerResultEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.time, datetime.date)):
            return obj.isoformat()
        if isinstance(obj, bytes):
            return "Result type bytes, not supported yet."
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class Task:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.result = dict()
        # Initialize to gracefully fail unless successful.
        self.state = "ERROR"
        self.state_info = "Unhandled error during execution."
        self.output = {"error": self.state_info}

    def read_input_file(self):
        # load parameters
        with open(self.input_file_path) as input_file:
            self.input = json.load(input_file)

        self.working_dir = os.path.dirname(os.path.abspath(self.input_file_path))

        self.action = self.input["action"]
        self.pack = self.input["pack"]
        self.config_path = self.input["config_path"]
        self.execution_id = self.input["action_context"]["njinn_execution_id"]

    def load_action(self):
        # import action (try)
        action_entry_point = self.action.split(":")
        if len(action_entry_point) != 2:
            raise Exception(
                f"Entrypoint(path) misconfigured, missing ':'. '{self.action}' should look like this 'folder.file:class'"
            )
        action_module = action_entry_point[0]
        action_class_name = action_entry_point[1]

        module = f"packs.{self.pack}.{action_module}"
        mod = importlib.import_module(module)
        action_class = getattr(mod, action_class_name)

        self.action = action_class()

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)

        self.njinn_api = config["DEFAULT"]["njinn_api"]
        self.secret = config["DEFAULT"]["secret"]
        self.worker_name = config["DEFAULT"]["name"]
        self.secrets_key = config["DEFAULT"]["secrets_key"]

    def load_njinn_api(self):
        self.njinn = NjinnAPI(
            self.njinn_api, self.secret, self.worker_name, self.execution_id
        )
        setattr(self.action, "_njinn", self.njinn)

    def decrypt_secret_value(self, value, pattern=r"SECRET\(([-A-Za-z0-9+_=]+)\)"):
        """
        Looks for an encrypted variable and decrypt if found and
        also replaces it with the decrypted variable in ``value``.
        """

        original_value = value
        value_log = str(original_value)

        if isinstance(original_value, dict):
            value = {}
            value_log = {}
            for k, v in original_value.items():
                value[k], value_log[k] = self.decrypt_secret_value(v)
        elif isinstance(original_value, str):
            secret_values = re.findall(pattern, value)
            if secret_values:
                for secret_value in secret_values:
                    f = Fernet(self.secrets_key)
                    encrypted_variable = secret_value.encode()

                    try:
                        variable = f.decrypt(encrypted_variable).decode()
                        value = re.sub(pattern, variable, value, count=1)
                    except InvalidToken:
                        print("Invalid token for decryption of secret values.")

                value_log = re.sub(pattern, "*" * 6, original_value)

        if len(value_log) > 40:
            value_log = value_log[:40] + "..."

        return value, value_log

    def prep_files_from_storage(self, value, pattern=r"FILE\(([0-9]+)\)"):
        """
        Looks for a file reference and downloads it. If found, replace the
        reference with the temp path to the file.
        """

        original_value = value

        if isinstance(original_value, dict):
            value = {}
            value_log = {}
            for k, v in original_value.items():
                value[k] = self.prep_files_from_storage(v)
        elif isinstance(original_value, str):
            files = re.findall(pattern, value)
            if files:
                for file in files:
                    file_path = self.njinn.download_file(file, self.working_dir)
                    value = re.sub(pattern, file_path, value, count=1)

        return value

    def set_action_parameters(self):
        params = self.input["action_context"]["parameters"]

        for param, value in params.items():
            value = self.prep_files_from_storage(value)
            value, value_log = self.decrypt_secret_value(value)

            setattr(self.action, param, value)

    def write_output_file(self):
        # writes self.stdout, self.stderr, self.run_return, ... to output file
        self.result["output"] = self.output
        self.result["state"] = self.state
        self.result["state_info"] = self.state_info

        with open(os.path.join(self.working_dir, "out.json"), "w") as fp:
            json.dump(self.result, fp, cls=WorkerResultEncoder)

    def setup_signals(self):
        """
        Sets up handler to process signals from the OS.
        """

        def signal_handler(signum, frame):
            """Setting kill signal handler"""
            self.action.on_kill()
            raise Exception("Task received SIGTERM signal")

        signal.signal(signal.SIGTERM, signal_handler)

    def run_action(self):

        error = None
        try:
            self.read_input_file()
            self.load_action()
            self.load_config()
            self.load_njinn_api()
            self.set_action_parameters()
            self.setup_signals()

            os.chdir(self.working_dir)

            # When someone exit()s the script, this will jump to the finally block
            # Ensure proper status handling.
            error = "Action execution interrupted. exit() called?"

            action_return = self.action.run()
            error = None

            # defaults are task failure - unset output, state and state_info
            if action_return is not None:
                if isinstance(action_return, dict):
                    self.output = action_return
                else:
                    self.output = {"result": action_return}
            else:
                self.output = None
            self.state = "SUCCESS"

            self.state_info = None
        except KeyboardInterrupt as e:
            error = traceback.format_exc()
        except Exception as e:
            # We assume that actions provide meaningful messages
            # but will to show a traceback if this is not the case.
            error = str(e)
            if error == "" or error == "None":
                error = traceback.format_exc()
        finally:
            if error is not None:
                # explicit error handling
                self.state_info = error
                self.output = {"error": self.state_info}
                self.state = "ERROR"
                print("Error:")
                print(self.state_info)
            self.write_output_file()


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(
            "Invalid call. Require exactly one argument, which is the path to the inputfile."
        )
        sys.exit(1)

    task = Task(sys.argv[1])
    task.run_action()
