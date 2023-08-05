"""
Copyright (C) JheysonDev ~ All right reserved
"""
import os
import platform


class Config:
    def __init__(
        self, 
        prompt="-| ",
        prompt_color="BLUE",
    ):
        self.prompt: str = str(prompt)
        self.prompt_color: str = str(prompt_color.upper())
        self.commands: dict
        self.home_path: str = ""
        self.platform_name: str = ""
        self.caths_paths: list = [""]

    def run(self):
        self.platform()
        self.paths()

    def platform(self):
        self.platform_name = platform.system()

    def paths(self):
        if self.platform_name == "Linux" or "Darwin":
            self.home_path = os.path.expanduser("~")
        elif self.platform_name == "Windows":
            self.home_path = os.path.expanduser("%USERPROFILE%")
        self.caths_paths = [
            "{0}/.catsh/".format(self.home_path),
            "{0}/.catsh/config.py".format(self.home_path),
            "{0}/.catsh/logs/".format(self.home_path),
            "{0}/.catsh/tmp/".format(self.home_path),
            "{0}/.catsh/plugins/".format(self.home_path),
        ]
        for p in  self.caths_paths:
            if os.path.exists(p) is False:
                if p.endswith("/"):
                    os.mkdir(p)
                else:
                    file = open(p, "w")
                    if p.endswith("config.py"):
                        file.write(
                            "# Welcome to Catsh config file\nfrom Catsh import config"
                        )
            else:
                return


config = Config()
config.run()