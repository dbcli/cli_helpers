from cli_helpers.packages import tabulate
from .preprocessors import bytes_to_string, align_decimals

supported_markup_formats = ('mediawiki', 'html', 'latex', 'latex_booktabs',
                            'textile', 'moinmoin', 'jira')
supported_table_formats = ('plain', 'simple', 'grid', 'fancy_grid', 'pipe',
                           'orgtbl', 'psql', 'rst')
supported_formats = supported_markup_formats + supported_table_formats

preprocessors = (bytes_to_string, align_decimals)


def adapter(data, headers, table_format=None, missing_value='',
            disable_numparse=False, preserve_whitespace=False, **_):
    """Wrap tabulate inside a function for TabularOutputFormatter."""
    kwargs = {'tablefmt': table_format, 'missingval': missing_value,
              'disable_numparse': disable_numparse}
    if table_format in supported_markup_formats:
        kwargs.update(numalign=None, stralign=None)

    tabulate.PRESERVE_WHITESPACE = preserve_whitespace

    return tabulate.tabulate(data, headers, **kwargs)
