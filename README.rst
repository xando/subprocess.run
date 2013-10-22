==========================
from subprocess import run
==========================

The **subprocess** extension to run processes.


.. code-block:: python

   >>> from subprocess import run

   >>> run('uname -r').stdout
   3.7.0-7-generic

   >>> run('uname -a').status
   0

   >>> print run('rm not_existing_directory').stderr
   rm: cannot remove `not_existing_directory': No such file or directory

   >>> print run('ls -la', 'wc -l')
   14


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

to test it, launch **python**

.. code-block:: python

   >>> from subprocess import run


Supported platforms
-------------------

* Python2.6
* Python2.7
* Python3.3
* PyPy2.1


Tests
-----

.. image:: https://travis-ci.org/xando/subprocess.run.png?branch=master
   :target: https://travis-ci.org/xando/subprocess.run

.. code-block:: bash

   >>> python setup.py test
