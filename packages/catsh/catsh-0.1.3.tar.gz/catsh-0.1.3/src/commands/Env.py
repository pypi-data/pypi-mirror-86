"""
Copyright (C) JheysonDev ~ All right reserved
"""
import os


class EnvCommand:
    def __init__(self, args: str):
        self.args = args.split(" ", 1)
        self.env_name = self.args[0]
        self.env_value = ""

    def run(self):
        if len(self.args) == 2:
            self.env_value = self.args[1]
        if self.env_value <= "":
            print(os.getenv(self.env_name))
        if self.env_value >= "":
            os.environ[self.env_name] = self.env_value
