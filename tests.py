import sys
import pytest
import subprocess

from functools import partial

from run import run

unix = pytest.mark.skipif(
    not (sys.platform.startswith('linux') or sys.platform.startswith('darwin')),
    reason="Unix test"
)

# dafault _commands
class _commands:
    ls = 'ls -la'
    rm = 'rm -r'
    more = 'more'

# override _commands for windows plaftorm
if sys.platform.startswith('win'):
    class _commands:
        ls = 'dir'
        rm = 'rmdir'
        more = 'more'


def test_run():
    output = run(_commands.ls)

    assert output.lines
    assert output

    assert isinstance(output.lines, list)
    assert isinstance(output.qlines, list)
    assert isinstance(output.qlines[0], list)


def test_stdout():
    assert run(_commands.ls).stdout.lines
    assert run(_commands.ls).stdout


def test_stderr():
    assert run('%s not_existing_directory' % _commands.rm).stderr
    assert run('%s not_existing_directory' % _commands.rm).stderr.lines


def test_status():
    assert run(_commands.ls).status == 0
    # win workaround
    assert run('%s not_existing_directory' % _commands.rm).status != 0


def test_chain():
    command = run('ps aux', 'wc -l', 'wc -c')

    assert command.status == 0
    assert len(run('ps aux', 'wc -l', 'wc -c').chain) == 3
    assert [0, 0, 0] == [e.status for e in run('ps aux', 'wc -l', 'wc -c').chain]
    assert [1, 0] == [e.status for e in run('ps aux fail', 'wc -l').chain]


Popen = partial(
    subprocess.Popen,
    universal_newlines=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

@unix
def test_popen_1():
    command = Popen(['ls'])

    assert command.communicate()[0] == run('ls').stdout


@unix
def test_popen_2():
    command = Popen(['ls', '-la'])

    assert command.communicate()[0] == run('ls -la').stdout


@unix
def test_popen_3():
    command = Popen(['ls', '-la'])
    command = Popen(['wc', '-c'], stdin=command.stdout)

    assert command.communicate()[0] == run('ls -la', 'wc -c').stdout


@unix
def test_popen_4():

    command = Popen(['cat', '/dev/urandom'])
    command = Popen(['tr', '-dc', '"[:alpha:]"'], stdin=command.stdout)
    command = Popen(["head", "-c", "10"], stdin=command.stdout)

    assert len(command.communicate()[0]) == \
        len(run("cat /dev/urandom", 'tr -dc "[:alpha:]"', "head -c 10").stdout)


def test_stdin():
    command = run(
        "ls -la",
        """python -c 'from run import run; print(run("wc -l", stdin=run.stdin).stdout)'"""
    )

    command.stdout.strip("\n") == run('ls -la', 'wc -l')