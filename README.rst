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


To use pipe from the shell.

.. code-block:: python

  from subprocess import run
  run('grep something', data=run.stdin)

.. code-block:: bash

  $ ps aux | python script.py


Install
-------

You can install it from PyPi, by simply **pip**:

.. code-block:: bash

   $ pip install subprocess.run

only if you don't have pip installed, an alternative method is **easy_install**:

.. code-block:: bash

   $ easy_install subprocess.run

to test it, launch **python**

.. code-block:: python
   
   >>> from subprocess import run


Supported platforms
-------------------

* Python2.6
* Python2.7
* Python3.3
* PyPy1.9
