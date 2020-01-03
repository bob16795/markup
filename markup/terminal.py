import click


class error:
    def __init__(self, message=""):
        self.message = message

    def report(self):
        return click.style("ERROR: %s" % self.message, fg='red', bold=True), 0


class warn:
    def __init__(self, message=""):
        self.message = message

    def report(self):
        return click.style("WARNING: %s" % self.message, fg='red'), 1


class log:
    def __init__(self, message=""):
        self.message = message

    def report(self):
        return "LOG: %s" % self.message, 2


class info:
    def __init__(self, message=""):
        self.message = message

    def report(self):
        return "INFO: %s" % self.message, 3


class debug:
    def __init__(self, message=""):
        self.message = message

    def report(self):
        return "DEBUG %s" % self.message, 4


class terminal:
    def __init__(self, verbosity):
        self.verbosity = verbosity

    def add(self, type_class, message):
        message_class = type_class(message)
        output, result = message_class.report()
        if self.verbosity >= result:
            if result == 0:
                click.echo(output)
                quit(code=1)
            else:
                click.echo(output)
