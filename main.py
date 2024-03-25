from models import TTS
import os
from commands.ai import GPTCommand, VisionCommand, TTSCommand
from commands.basic import HelloCommand, ExitCommand
import dotenv

dotenv.load()


class Logger:
    def __init__(self):
        self.tts_model = TTS() if "TTS" in os.environ else None

    def __call__(self, output):
        if self.tts_model:
            self.tts_model(output)
        print(output)


class Mode:
    def __init__(self):
        self.title = "Base Mode"
        self.commands = []

    def enter(self):
        print(self.title)


class MainMode(Mode):
    def __init__(self):
        self.title = "Welcome to Guru. Type 'exit' to quit."
        self.logger = Logger()
        self.commands = [
            HelloCommand(logger=self.logger),
            ExitCommand(logger=self.logger),
            GPTCommand(logger=self.logger),
            VisionCommand(logger=self.logger),
            TTSCommand(),
        ]
        self.commands_dict = {command.name: command for command in self.commands}

    def process_command(self, *args):
        try:
            command = self.commands_dict[args[0]]
            command.execute(*args)
        except KeyError:
            print("Invalid command. Valid commands:\n")
            self.print_valid_commands()

    def print_valid_commands(self):
        [print(f"{cmd.name}") for cmd in self.commands]


def main():
    mode = MainMode()
    mode.enter()
    try:
        while True:
            command = input(">>> ").strip()
            command_args = command.split()
            if len(command_args) > 0:
                mode.process_command(*command_args)
    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
