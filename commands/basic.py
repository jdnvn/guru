from commands.base import Command


class HelloCommand(Command):
    def init(self):
        self.name = "hello"

    def _execute(self, *args):
        self.logger("Hello there!")


class ExitCommand(Command):
    def init(self):
        self.name = "exit"

    def _execute(self, *args):
        self.logger("Goodbye!")
        exit(1)
