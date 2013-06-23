==========================
from subprocess import run
==========================

The **subprocess** extension to run processes.


.. code-block:: python


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


Status
------

Library seems to be pretty stable. Feel free to use it as you want. 
But this may not be the final version of the API. 


Install
-------

You can install it from PyPi, by simply using **pip**:

.. code-block:: bash

   $ pip install suprocess.run

(only if you don't have pip installed), an alternative method use **easy_install**:

.. code-block:: bash

   $ easy_install suprocess.run

to test it launch **python**

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
