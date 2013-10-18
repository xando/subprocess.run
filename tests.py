import sys


from run import run


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


def test_pipe():
    assert run(_commands.ls, _commands.more).status == 0


def test_chain():
    command = run('ps aux', 'wc -l', 'wc -c')
    # print command.chain
    assert command.status == 0
    assert len(run('ps aux', 'wc -l', 'wc -c').chain) == 3
    assert [0, 0, 0] == [e.status for e in run('ps aux', 'wc -l', 'wc -c').chain]

    assert [1, 0] == [e.status for e in run('ps aux fail', 'wc -l').chain]
