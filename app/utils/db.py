def select(db, table, columns, where=None, order_by=None, limit=None, args=()):
    """Select rows from a table.

    Args:
        db (sqlite3.Connection): database connection
        table (str): table name
        columns (list): list of columns to select
        where (str, optional): where clause. Defaults to None.
        order_by (str, optional): order by clause. Defaults to None.
        limit (int, optional): limit clause. Defaults to None.
        args (tuple, optional): arguments for where clause. Defaults to ().

    Returns:
        list: list of rows
    """
    columns = ", ".join(columns)
    query = f"SELECT {columns} FROM {table}"

    if where:
        query += f" WHERE {where}"

    if order_by:
        query += f" ORDER BY {order_by}"

    if limit:
        query += f" LIMIT {limit}"

    rows = db.execute(query, args).fetchall()

    rows = [dict(row) for row in rows]

    return rows