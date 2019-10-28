import threading
import click

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
  def compile(verbose, prop, file, tree=False):
    from markup.commands import _read, _compile, _output
    if verbose >= 1:
        click.echo(f"started {file}")
    text = _read(file, verbose)
    text, prop_slave = _compile(
        text, verbose, "", file, tree)
    if not tree:
        if text != "":
            _output(text, file, prop_slave, verbose)
  
  def finish(self, verbose):
    for index, thread in enumerate(self.threads):
      if verbose >= 4:
        click.echo(f"started thread {index}")
      thread.start()
    for thread in self.threads:
      thread.join()
    if verbose >= 4:
      click.echo(f"finished {self.threads.__len__()} threads")
    self.threads = list()
