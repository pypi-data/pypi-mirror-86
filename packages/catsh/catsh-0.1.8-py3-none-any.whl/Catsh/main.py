"""
Copyright (C) JheysonDev ~ All right reserved
"""
from Catsh.commands import Close, Clean, Print, Exec, Env
from Catsh.utils import Error
from colorama import Fore


class Main:
    def __init__(self, prompt="-| "):
        self.prompt = prompt
        self.cli: str = input(self.prompt)

    def run(self):
        self.shell()

    def shell(self):
        while self.cli >= "":
            command: list = self.cli.split(" ", 1)
            if command[0] == "print":
                Print.PrintCommand(command[1]).run()
            elif command[0] == "clean":
                Clean.CleanCommand().run()
            elif command[0] == "close":
                Close.CloseCommand().run()
            elif command[0] == "exec":
                Exec.ExecCommand(command[1]).run()
            elif command[0] == "env":
                Env.EnvCommand(command[1]).run()
            elif command[0] == "":
                Error.Error("You must enter a command").run()
            else:
                Error.Error("Command no found").run()
            self.cli = input(self.prompt)


if __name__ == "__main__":
    main = Main()
    run = main.run()
