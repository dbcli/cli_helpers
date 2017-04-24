Quickstart
==========

Displaying Tabular Data
-----------------------


The Basics
++++++++++

CLI Helpers provides a simple way to display your tabular data (columns/rows) in a visually-appealing manner::

    >>> from cli_helpers import tabular_output

    >>> data = [[1, 'Asgard', True], [2, 'Camelot', False], [3, 'El Dorado', True]]
    >>> headers = ['id', 'city', 'visited']

    >>> print(tabular_output.format_output(data, headers, format_name='simple'))

      id  city       visited
    ----  ---------  ---------
       1  Asgard     True
       2  Camelot    False
       3  El Dorado  True

Let's take a look at what we did there.

1. We imported the :mod:`~cli_helpers.tabular_output` module. This module gives us access to the :func:`~cli_helpers.tabular_output.format_output` function.

2. Next we generate some data. Plus, we need a list of headers to give our data some context.

3. We format the output using the display format ``simple``. That's a nice looking table!


Display Formats
+++++++++++++++

To display your data, :mod:`~cli_helpers.tabular_output` uses
`tabulate <https://bitbucket.org/astanin/python-tabulate>`_,
`terminaltables <https://robpol86.github.io/terminaltables/>`_, :mod:`csv`,
and its own vertical table layout.

The best way to see the various display formats is to use the
:class:`~cli_helpers.tabular_output.TabularOutputFormatter` class. This is
what the :func:`~cli_helpers.tabular_output.format_output` function in our
first example uses behind the scenes.

Let's get a list of all the supported format names::

    >>> from cli_helpers.tabular_output import TabularOutputFormatter
    >>> formatter = TabularOutputFormatter()
    >>> formatter.supported_formats
    ('vertical', 'csv', 'tsv', 'mediawiki', 'html', 'latex', 'latex_booktabs', 'textile', 'moinmoin', 'jira', 'plain', 'simple', 'grid', 'fancy_grid', 'pipe', 'orgtbl', 'psql', 'rst', 'ascii', 'double', 'github')

You can format your data in any of those supported formats. Let's take the
same data from our first example and put it in the ``fancy_grid`` format::

    >>> data = [[1, 'Asgard', True], [2, 'Camelot', False], [3, 'El Dorado', True]]
    >>> headers = ['id', 'city', 'visited']
    >>> print(formatter.format_output(data, headers, format_name='fancy_grid'))
    ╒══════╤═══════════╤═══════════╕
    │   id │ city      │ visited   │
    ╞══════╪═══════════╪═══════════╡
    │    1 │ Asgard    │ True      │
    ├──────┼───────────┼───────────┤
    │    2 │ Camelot   │ False     │
    ├──────┼───────────┼───────────┤
    │    3 │ El Dorado │ True      │
    ╘══════╧═══════════╧═══════════╛

That was easy! How about CLI Helper's vertical table layout?

    >>> print(formatter.format_output(data, headers, format_name='vertical'))
    ***************************[ 1. row ]***************************
    id      | 1
    city    | Asgard
    visited | True
    ***************************[ 2. row ]***************************
    id      | 2
    city    | Camelot
    visited | False
    ***************************[ 3. row ]***************************
    id      | 3
    city    | El Dorado
    visited | True


Default Format
++++++++++++++

When you create a :class:`~cli_helpers.tabular_output.TabularOutputFormatter`
object, you can specify a default formatter so you don't have to pass the
format name each time you want to format your data::

    >>> formatter = TabularOutputFormatter(format_name='plain')
    >>> print(formatter.format_output(data, headers))
      id  city       visited
       1  Asgard     True
       2  Camelot    False
       3  El Dorado  True

.. TIP::
   You can get or set the default format whenever you'd like through
   :data:`TabularOutputFormatter.format_name <cli_helpers.tabular_output.TabularOutputFormatter.format_name>`.


Passing Options to the Formatters
+++++++++++++++++++++++++++++++++

Many of the formatters have settings that can be tweaked by passing
an optional argument when you format your data. For example,
if we wanted to enable or disable number parsing on any of
`tabulate's <https://bitbucket.org/astanin/python-tabulate>`_
formats, we could::

    >>> data = [[1, 1.5], [2, 19.605], [3, 100.0]]
    >>> headers = ['id', 'rating']
    >>> print(format_output(data, headers, format_name='simple', disable_numparse=True))
    id    rating
    ----  --------
    1     1.5
    2     19.605
    3     100.0
    >>> print(format_output(data, headers, format_name='simple', disable_numparse=False))
      id    rating
    ----  --------
       1     1.5
       2    19.605
       3   100


Lists and tuples and bytearrays. Oh my!
+++++++++++++++++++++++++++++++++++++++

:mod:`~cli_helpers.tabular_output` supports any :term:`iterable`, not just
a :class:`list` or :class:`tuple`. You can use a :class:`range`,
:func:`enumerate`, a :class:`str`, or even a :class:`bytearray`! Here is a
far-fetched example to prove the point::

    >>> step = 3
    >>> data = [range(n, n + step) for n in range(0, 9, step)]
    >>> headers = 'abc'
    >>> print(format_output(data, headers, format_name='simple'))
      a    b    c
    ---  ---  ---
      0    1    2
      3    4    5
      6    7    8

Real life examples include a PyMySQL
:class:`Cursor <pymysql:pymysql.cursors.Cursor>` with
database results or
NumPy :class:`ndarray <numpy:numpy.ndarray>` with data points.
