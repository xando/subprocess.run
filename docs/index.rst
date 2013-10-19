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

   >>> run('uname -r').stdout
   'Linux lena-laptop 3.11.0-12-generic #19-Ubuntu SMP Wed Oct 9 16:20:46 UTC 2013 x86_64 x86_64 x86_64 GNU/Linux'

   >>> run('uname -a').status
   0

   >>> run('rm not_existing_directory').stderr
   rm: cannot remove `not_existing_directory': No such file or directory

   >>> run('ls -la', 'wc -l')
   14

   >>> run('ls -la', 'wc -l', 'wc -c')
   3

   >>> run('ls -la', 'wc -l', 'wc -c')
   ls -la | wc -l | wc -c

   >>> run('ls -la').stdout.lines
   ['total 20',
   'drwxrwxr-x 3 user user 4096 Dec 20 22:55 .',
   'drwxrwxr-x 5 user user 4096 Dec 20 22:57 ..',
   'drwxrwxr-x 2 user user 4096 Dec 20 22:37 dir',
   '-rw-rw-r-- 1 user user    0 Dec 20 22:52 file']


Status
------

The Code base is less than 100 LOC, feel free to look at it and explain to me why I should/shouldn't do things this way. 
Library seems to be pretty stable. Feel free to use it as you want. But this may not be the final version of the API. 


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
