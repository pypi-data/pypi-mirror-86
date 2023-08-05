"""
Copyright (C) JheysonDev ~ All right reserved
"""
import os
from utils import Error


class EnvCommand:
    def __init__(self, args: str):
        self.args: list = args.split(" ", 1)
        self.env_name: str = self.args[0]
        self.env_value: str = ""

    def run(self):
        if len(self.args) == 2:
            self.env_value = self.args[1]
        if self.env_value <= "":
            if os.getenv(self.env_name) is None:
                Error.Error("Environment variable does not exist").run()
            else:
                print(os.getenv(self.env_name))
        if self.env_value >= "":
            os.environ[self.env_name] = self.env_value
