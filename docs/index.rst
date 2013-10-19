==========================
from subprocess import run
==========================

Python’s standard **subprocess** module provides most of the capabilities you need to run external processes from Python, but the API is thoroughly misleading. 
It requires you to check documentation every time when you are trying to do really simple thing like calling external process.

The **subprocess.run** extension was create to run processes in a polite way. Bellow is short walk through, what is possible with **subprocess.run**.


Walkthrough 
-----------

.. code-block:: python

   >>> from subprocess import run

If installation went successful, import **run** from **subprocess** module.

.. code-block:: python

   >>> run('uname -v').stdout
   '#19-Ubuntu SMP Wed Oct 9 16:20:46 UTC 2013'

The standard output (successful command output) is available thought the **stdout** attribute.

.. code-block:: python

   >>> run('uname -v').status
   0

You can access execution status through **status** attribute.

.. code-block:: python

   >>> run('rm not_existing_directory').stderr
   'rm: cannot remove `not_existing_directory': No such file or directory'

If something went not so well, the error output is available thought the **stderr** attribute.

.. code-block:: python

   >>> run('ls -la', 'wc -l')
   14

If pipe is needed, just add more one after another. Example above is same thins as **ls -la | wc -l**.

.. code-block:: python

   >>> run('ls -la', 'wc -l', 'wc -c')
   3

And more pipe.

.. code-block:: python

   >>> run('wc -c', data="test")

And even more pipe. But this time, the call will take data from python script. This would be roughly something more or less like **echo test | wc -c**


.. code-block:: python

   >>> run('ls -la').stdout.lines
   ['total 20',
   'drwxrwxr-x 3 user user 4096 Dec 20 22:55 .',
   'drwxrwxr-x 5 user user 4096 Dec 20 22:57 ..',
   'drwxrwxr-x 2 user user 4096 Dec 20 22:37 dir',
   '-rw-rw-r-- 1 user user    0 Dec 20 22:52 file']

To help with output processing, both **stdout** and **stderr** outputs are equipped with **lines** and **qlines** attribute, it will help with slicing your output to a list of strings.

   >>> run('ls -la').stdout.qlines
   [
      ['total 20']
      ['drwxrwxr-x', '3', 'user', 'user', '4096', 'Dec', '20', '22:55', '.'],
      ['drwxrwxr-x', '5', 'user', 'user', '4096', 'Dec', '20', '22:57', '..'],
      ['drwxrwxr-x', '2', 'user', 'user', '4096', 'Dec', '20', '22:37', 'dir'],
      ['-rw-rw-r--', '1', 'user', 'user', '0', 'Dec', '20', '22:52', 'file']
   ]

And with **qlines** if you want to take this idea even further.

Status
------

The codebase is less than 100 LOC, feel free to look at it and explain to me why I should/shouldn't do things this way. Library seems to be pretty stable. Feel free to use it as you want.

Install
-------

You can install it from PyPi, by simply using **pip**:

.. code-block:: bash

   $ pip install suprocess.run

to test your installation just launch **python** and

.. code-block:: python
   
   >>> from suprocess import run


Supported platforms
-------------------

* Python2.6
* Python2.7
* Python3.3
* PyPy1.9


Source Code
-----------

https://github.com/xando/subprocess.run


API
---

:mod:`suprocess.run` -- subprocess wrapper
-------------------------------------------
.. py:module:: run.run

.. code-block:: python

   >>> from subprocess import run

   >>> run('uname -r').stdout
   3.7.0-7-generic

   >>> run('uname -r', 'wc -c')
   uname -r | wc -c

   >>> run('uname -r', 'wc -c').stdout
   16


.. py:attribute:: run.stdout

   Standard output from executed command

   .. code-block:: python

      >>> run('uname -r').stdout
      3.7.0-7-generic

      >>> run('ls -la').stdout.lines
      ['total 20',
       'drwxrwxr-x 3 user user 4096 Dec 20 22:55 .',
       'drwxrwxr-x 5 user user 4096 Dec 20 22:57 ..',
       'drwxrwxr-x 2 user user 4096 Dec 20 22:37 dir',
       '-rw-rw-r-- 1 user user    0 Dec 20 22:52 file']

      >>> run('ls -la').stdout.qlines
      [['total 20'],
       ['drwxrwxr-x, 3, user, user, 4096, Dec, 20, 22:55, .'],
       ['drwxrwxr-x, 5, user, user, 4096, Dec, 20, 22:57, ..'],
       ['drwxrwxr-x, 2, user, user, 4096, Dec, 20, 22:37, dir'],
       ['-rw-rw-r--, 1, user, user,    0, Dec, 20, 22:52, file']]


.. py:attribute:: run.stderr

   Standard error from executed command

   .. code-block:: python

      >>> run('rm not_existing_directory').stderr
      rm: cannot remove `not_existing_directory': No such file or directory


.. py:attribute:: run.status

   Status code of executed command

   .. code-block:: python

      >>> run('uname -r').status
      0

      >>> run('rm not_existing_directory').status
      1

.. py:attribute:: run.chain

   The full chain of command executed 

   .. code-block:: python

      >>> run('uname -r', 'wc -c').chain
      [uname -r | wc -c]

   To get statuses from all component commands

      >>> [e.status for e in run('uname -r', 'wc -c').chain]
      [0, 0]


.. py:attribute:: run.pipe

To pipe data in

.. code-block:: python

    from subprocess import run

    run('grep something', data=run.stdin)

.. code-block:: bash

      $ ps aux | python script.py


-----
