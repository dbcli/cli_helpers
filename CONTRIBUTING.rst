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

   We've just created a virtual environment that we'll use to install all the dependencies
   and tools we need to work on CLI Helpers. Whenever you want to work on CLI Helpers, you
   need to activate the virtual environment::

    $ source cli_helpers_dev/bin/activate

   When you're done working, you can deactivate the virtual environment::

    $ deactivate

5. Install the dependencies and development tools::

    $ pip install -r requirements-dev.txt
    $ pip install --editable .

6. Create a branch for your bugfix or feature based off the ``master`` branch::

    $ git checkout -b <name-of-bugfix-or-feature> master

7. While you work on your bugfix or feature, be sure to pull the latest changes from ``upstream``. This ensures that your local codebase is up-to-date::

    $ git pull upstream master

8. When your work is ready for the CLI Helpers team to review it, push your branch to your fork::

    $ git push origin <name-of-bugfix-or-feature>

9. `Create a pull request <https://help.github.com/articles/creating-a-pull-request-from-a-fork/>`_
   on GitHub.


Running the Tests
-----------------

While you work on CLI Helpers, it's important to run the tests to make sure your code
hasn't broken any existing functionality. To run the tests, just type in::

    $ pytest

CLI Helpers supports Python 2.7 and 3.4+. You can test against multiple versions of
Python by running::

    $ tox

You can also measure CLI Helper's test coverage by running::

    $ pytest --cov-report= --cov=cli_helpers
    $ coverage report


Coding Style
------------

CLI Helpers requires code submissions to adhere to
`PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_.
It's easy to check the style of your code, just run::

    $ pep8radius master

If you see any PEP 8 style issues, you can automatically fix them by running::

    $ pep8radius master --in-place

Be sure to commit and push any PEP 8 fixes.


Documentation
-------------

If your work in CLI Helpers requires a documentation change or addition, you can
build the documentation by running::

    $ make -C docs clean html
    $ open docs/build/html/index.html

That will build the documentation and open it in your web browser.
