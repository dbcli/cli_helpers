How to Contribute
=================

CLI Helpers would love your help! We appreciate your time and always give credit.

Development Setup
-----------------

Ready to contribute? Here's how to set up CLI Helpers for local development.

1. `Fork the repository <https://github.com/dbcli/cli_helpers>`_ on GitHub.
2. Clone your fork locally::

    $ git clone <url-for-your-fork>

3. Add the official repository (``upstream``) as a remote repository::

    $ git remote add upstream git@github.com:dbcli/cli_helpers.git

4. Set up a `virtual environment <http://docs.python-guide.org/en/latest/dev/virtualenvs>`_
   for development::

    $ cd cli_helpers
    $ pip install virtualenv
    $ virtualenv cli_helpers_dev

   We've just created a virtual environment called ``cli_helpers_dev``
   that we'll use to install all the dependencies and tools we need to work on CLI Helpers.
   Whenever you want to work on CLI Helpers, you need to activate the virtual environment::

    $ source cli_helpers_dev/bin/activate

   When you're done working, you can deactivate the virtual environment::

    $ deactivate

5. From within the virtual environment, install the dependencies and development tools::

    $ pip install -r requirements-dev.txt
    $ pip install --editable .

6. Create a branch for your bugfix or feature based off the ``master`` branch::

    $ git checkout -b <name-of-bugfix-or-feature> master

7. While you work on your bugfix or feature, be sure to pull the latest changes from ``upstream``.
   This ensures that your local codebase is up-to-date::

    $ git pull upstream master

8. When your work is ready for the CLI Helpers team to review it,
   make sure to add an entry to CHANGELOG file, and add your name to the AUTHORS file.
   Then, push your branch to your fork::

    $ git push origin <name-of-bugfix-or-feature>

9. `Create a pull request <https://help.github.com/articles/creating-a-pull-request-from-a-fork/>`_
   on GitHub.


Running the Tests
-----------------

While you work on CLI Helpers, it's important to run the tests to make sure your code
hasn't broken any existing functionality. To run the tests, just type in::

    $ pytest

CLI Helpers supports Python 3.6+. You can test against multiple versions of
Python by running::

    $ tox

You can also measure CLI Helper's test coverage by running::

    $ pytest --cov-report= --cov=cli_helpers
    $ coverage report


Coding Style
------------

When you submit a PR, the changeset is checked for pep8 compliance using
`black <https://github.com/psf/black>`_. If you see a build failing because
of these checks, install ``black`` and apply style fixes:

::

    $ pip install black
    $ black .

Then commit and push the fixes.

To enforce ``black`` applied on every commit, we also suggest installing ``pre-commit`` and
using the ``pre-commit`` hooks available in this repo:

::

    $ pip install pre-commit
    $ pre-commit install

Git blame
---------

Use ``git blame my_file.py --ignore-revs-file .git-blame-ignore-revs`` to exclude irrelevant commits
(specifically Black) from ``git blame``. For more information,
see `here <https://github.com/psf/black#migrating-your-code-style-without-ruining-git-blame>`_.

Documentation
-------------

If your work in CLI Helpers requires a documentation change or addition, you can
build the documentation by running::

    $ make -C docs clean html
    $ open docs/build/html/index.html

That will build the documentation and open it in your web browser.
