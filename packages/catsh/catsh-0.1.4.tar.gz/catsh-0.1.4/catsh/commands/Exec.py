"""
Copyright (C) JheysonDev ~ All right reserved
"""
import os
from utils import Error


class ExecCommand:
    def __init__(self, args=""):
        self.path: list = os.getenv("PATH").split(":")
        self.args: list = args.split(" ", 1)
        self.iterations: int = len(self.path)

    def run(self):
        for b in self.path:
            if os.path.exists("{0}/{1}".format(b, self.args[0])) is True:
                os.system("{0}/{1}".format(b, self.args[0]))
            else:
                self.iterations = self.iterations - 1
                if self.iterations == 0:
                    Error.Error(
                        "no executable with the name of '{0}' was found in the path".format(
                            self.args[0]
                        )
                    ).run()
