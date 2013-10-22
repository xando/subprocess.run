==========================
from subprocess import run
==========================

Python’s standard **subprocess** module provides most of the capabilities you need to run external processes from Python, but the API is thoroughly misleading. 
It requires you to check documentation every time when you are trying to do really basic things related to creating external processes.

The **subprocess.run** extension was create to run processes in a polite way. 


Walkthrough 
-----------

.. code-block:: bash

   $ > pip install subprocess.run

To install the package.

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

   >>> run('ls -la', 'wc -l').stdout
   14

If pipe is needed, just add more one after another. Example above is the same as **ls -la | wc -l**.

.. code-block:: python

   >>> run('ls -la', 'wc -l', 'wc -c').stdout
   3

And more pipe.

.. code-block:: python

   >>> run('wc -c', data="test").stdout

And even more pipe. But this time, the call will take data from python script. This would be roughly something like **echo test | wc -c**


.. code-block:: python

   >>> run('ls -la').stdout.lines
   ['total 20',
   'drwxrwxr-x 3 user user 4096 Dec 20 22:55 .',
   'drwxrwxr-x 5 user user 4096 Dec 20 22:57 ..',
   'drwxrwxr-x 2 user user 4096 Dec 20 22:37 dir',
   '-rw-rw-r-- 1 user user    0 Dec 20 22:52 file']

To help with output processing, both **stdout** and **stderr** outputs are equipped with **lines** attribute, it will help with slicing your output to a list of strings.

   >>> run('ls -la').stdout.qlines
   [
      ['total 20']
      ['drwxrwxr-x', '3', 'user', 'user', '4096', 'Dec', '20', '22:55', '.'],
      ['drwxrwxr-x', '5', 'user', 'user', '4096', 'Dec', '20', '22:57', '..'],
      ['drwxrwxr-x', '2', 'user', 'user', '4096', 'Dec', '20', '22:37', 'dir'],
      ['-rw-rw-r--', '1', 'user', 'user', '0', 'Dec', '20', '22:52', 'file']
   ]

And with **qlines**, to split lines to words.

.. code-block:: python

    from subprocess import run

    run('grep something', data=run.stdin)

.. code-block:: bash

   $ ps aux | python script.py

To read from shell pipe.

Status
------

The codebase is less than 100 LOC, feel free to look at it and explain to me why I should/shouldn't do things this way. Library seems to be pretty stable, feel free to use it as you want.

Source Code
-----------

https://github.com/xando/subprocess.run

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


-----
