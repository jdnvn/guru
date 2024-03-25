class Command:
    def __init__(self, logger=None):
        self.name = None
        self.min_args = 0
        self.logger = logger
        self.init()

    # optionally initialize extra arguments
    def init(self):
        pass

    def validate(func):
        def validator(self, *args):
            if len(args) - 1 < self.min_args:
                print(
                    f"Invalid number of arguments for {self.name}: minimum of {self.min_args} arguments needed."
                )
            else:
                func(self, *args)

        return validator

    def _execute(self):
        pass

    @validate
    def execute(self, *args):
        self._execute(*args)
