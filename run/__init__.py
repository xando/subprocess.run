"""
  >>> from subprocess import run

  >>> print run('uname -r')
  3.7.0-7-generic

  >>> print run('uname -r').stdout
  3.7.0-7-generic

  >>> run('uname -a').status
  0

  >>> print run('rm not_existing_directory').stderr
  rm: cannot remove `not_existing_directory': No such file or directory

  >>> print run('ls -la', 'wc -l')
  14

  >>> print run('ls -la', 'wc -l', 'wc -c')
  3

  >>> run('ls -la', 'wc -l', 'wc -c')
  ls -la | wc -l | wc -c

  >>> print run('ls -la').stdout.lines
  ['total 20',
   'drwxrwxr-x 3 user user 4096 Dec 20 22:55 .',
   'drwxrwxr-x 5 user user 4096 Dec 20 22:57 ..',
   'drwxrwxr-x 2 user user 4096 Dec 20 22:37 dir',
   '-rw-rw-r-- 1 user user    0 Dec 20 22:52 file']


To use pipe from the shell.

.. code-block:: python

  from subprocess import run
  run('grep something', data=run.stdin)

.. code-block:: bash

  $ ps aux | python script.py

"""

import os
import sys
import shlex
import subprocess

__version__ = "0.0.7"


class std_output(str):

    @property
    def lines(self):
        return self.split("\n")

    @property
    def qlines(self):
        return [line.split() for line in self.split("\n")]


class runmeta(type):
    @property
    def stdin(cls):
        return sys.stdin


class run(runmeta('base_run', (std_output, ), {})):
    """

      >>> from subprocess import run

      >>> print run('uname -r')
      3.7.0-7-generic

      >>> print run('uname -r').stdout
      3.7.0-7-generic

      >>> run('uname -a').status
      0

      >>> print run('rm not_existing_directory').stderr
      rm: cannot remove `not_existing_directory': No such file or directory

      >>> print run('ls -la', 'wc -l')
      14

      >>> print run('ls -la', 'wc -l', 'wc -c')
      3

      >>> run('ls -la', 'wc -l', 'wc -c')
      ls -la | wc -l | wc -c

      >>> print run('ls -la').stdout.lines
      ['total 20',
       'drwxrwxr-x 3 user user 4096 Dec 20 22:55 .',
       'drwxrwxr-x 5 user user 4096 Dec 20 22:57 ..',
       'drwxrwxr-x 2 user user 4096 Dec 20 22:37 dir',
       '-rw-rw-r-- 1 user user    0 Dec 20 22:52 file']


    To use pipe from the shell.

    .. code-block:: python

      from subprocess import run
      run('grep something', data=run.stdin)

    .. code-block:: bash

      $ ps aux | python script.py

    """

    @classmethod
    def create_process(cls, command, stdin, cwd, env, shell):
        return subprocess.Popen(
            shlex.split(command),
            universal_newlines=True,
            shell=shell,
            cwd=cwd,
            env=env,
            stdin=stdin,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0,
        )

    def __new__(cls, *args, **kwargs):

        env = dict(os.environ)
        env.update(kwargs.get('env', {}))

        cwd = kwargs.get('cwd')
        shell = kwargs.get('shell', False)

        chain = []

        stdin = kwargs.get('stdin', subprocess.PIPE)

        for command in args:
            process = cls.create_process(command, stdin, cwd=cwd, env=env, shell=shell)

            stdin = process.stdout

            obj = super(run, cls).__new__(run, command)

            obj.process = process
            obj.pid = process.pid
            obj.command = command

            chain.append(obj)

            obj.chain = chain[:]

        return obj

    @property
    def status(self):
        self.process.communicate()
        return self.process.returncode

    @property
    def stdout(self):
        return std_output(self.process.communicate()[0])

    @property
    def stderr(self):
        return std_output(self.process.communicate()[1])

    def __repr__(self):
        return " | ".join([e.command for e in self.chain])


if __name__ == "__main__":
    pass
