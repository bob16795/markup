import threading
from markup.terminal import error, log, debug


class multi_tasker():
    """
    creates compiling workers and threads them
    """

    def __init__(self):
        self.threads = list()
        self.index = 0

    def add_to_queue(self, args):
        x = threading.Thread(target=self.compile, args=args)
        self.threads.append(x)

    @staticmethod
    def compile(output, file, tree=False):
        from markup.commands import _read, _compile, _output
        output.add(log, "started %s" % file)
        text = _read(file, output)
        text, prop_slave = _compile(
            text, output, "", file, tree)
        if not tree:
            if text != "":
                _output(text, file, prop_slave, output)

    def finish(self, output):
        for index, thread in enumerate(self.threads):
            output.add(debug, "threading.py: started thread %s" % index)
            thread.start()
        for thread in self.threads:
            thread.join()
        output.add(
            debug, "threading.py: finished %s threads" % self.threads.__len__())
        self.threads = list()
