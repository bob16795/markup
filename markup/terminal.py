import click


class error:
    def __init__(self, message=""):
        self.message = message

    def report(self):
        return click.style(f"ERROR: {self.message}", fg='red', bold=True), 0


class warn:
    def __init__(self, message=""):
        self.message = message

    def report(self):
        return click.style(f"WARNING: {self.message}", fg='red'), 1


class log:
    def __init__(self, message=""):
        self.message = message

    def report(self):
        return f"LOG: {self.message}", 2


class debug:
    def __init__(self, message=""):
        self.message = message

    def report(self):
        return f"DEBUG {self.message}", 3


class terminal:
    def __init__(self, verbosity):
        self.verbosity = verbosity

    def add(self, type_class, message):
        message_class = type_class(message)
        output, result = message_class.report()
        if self.verbosity >= result:
            if result == 0:
                click.echo(output)
                quit()
            else:
                click.echo(output)
