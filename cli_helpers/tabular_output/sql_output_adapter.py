# coding=utf-8

supported_formats = (
    "sql-insert",
    "sql-update",
    "sql-update-1",
    "sql-update-2",
)

preprocessors = ()


def escape_for_sql_statement(value):
    if isinstance(value, bytes):
        return f"X'{value.hex()}'"
    else:
        return "'{}'".format(value)


def adapter(data, headers, table_format=None, **kwargs):
    """
    This function registers supported_formats to default TabularOutputFormatter

    Parameters:
        data: query result
        headers: columns
        table_format: values from supported_formats
        kwargs:
            tables: parsed from clis
            delimeter: Character surrounds table name or column name when it conflicts with sql keywords.
                       For example, mysql uses ` and postgres uses "
    """
    # tables = extract_tables(formatter.query)
    tables = kwargs.get("tables")
    delimeter = kwargs.get("delimeter")
    if not isinstance(delimeter, str):
        delimeter = '"'

    if isinstance(tables, list) and len(tables) > 0:
        table = tables[0]
        if table[0]:
            table_name = "{}.{}".format(*table[:2])
        else:
            table_name = table[1]
    else:
        table_name = '{delimeter}DUAL{delimeter}'.format(delimeter=delimeter)

    header_joiner = '{delimeter}, {delimeter}'.format(delimeter=delimeter)
    if table_format == "sql-insert":
        h = header_joiner.join(headers)
        yield 'INSERT INTO {delimeter}{table_name}{delimeter} ({delimeter}{header}{delimeter}) VALUES'.format(
            table_name=table_name, header=h, delimeter=delimeter)
        prefix = "  "
        for d in data:
            values = ", ".join(escape_for_sql_statement(v) for i, v in enumerate(d))
            yield "{}({})".format(prefix, values)
            if prefix == "  ":
                prefix = ", "
        yield ";"
    if table_format.startswith("sql-update"):
        s = table_format.split("-")
        keys = 1
        if len(s) > 2:
            keys = int(s[-1])
        for d in data:
            yield 'UPDATE {delimeter}{table_name}{delimeter} SET'.format(table_name=table_name, delimeter=delimeter)
            prefix = "  "
            for i, v in enumerate(d[keys:], keys):
                yield '{prefix}{delimeter}{column}{delimeter} = {value}'.format(
                    prefix=prefix, delimeter=delimeter, column=headers[i], value=escape_for_sql_statement(v)
                )
                if prefix == "  ":
                    prefix = ", "
            f = '{delimeter}{column}{delimeter}" = {value}'
            where = (
                f.format(delimeter=delimeter, column=headers[i], value=escape_for_sql_statement(d[i]))
                for i in range(keys)
            )
            yield "WHERE {};".format(" AND ".join(where))



def register_new_formatter(TabularOutputFormatter):
    global formatter
    formatter = TabularOutputFormatter
    for sql_format in supported_formats:
        TabularOutputFormatter.register_new_formatter(
            sql_format, adapter, preprocessors, {"table_format": sql_format}
        )
