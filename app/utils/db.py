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


def insert(db, table, columns, values):
    """Insert a row into a table and get the id.

    Args:
        db (sqlite3.Connection): database connection
        table (str): table name
        columns (list): list of columns to insert
        values (list): list of values to insert

    Returns:
        int: id of inserted row
    """
    columns = ", ".join(columns)
    values_temp = ", ".join(["?"] * len(values))
    query = f"INSERT INTO {table} ({columns}) VALUES ({values_temp})"

    db.execute(query, values)
    db.commit()

    return db.execute("SELECT last_insert_rowid()").fetchone()[0]


def update(db, table, columns, values, where=None, args=()):
    """Update a row in a table.

    Args:
        db (sqlite3.Connection): database connection
        table (str): table name
        columns (list): list of columns to update
        values (list): list of values to update
        where (str): where clause
        args (tuple, optional): arguments for where clause. Defaults to ().
    """

    set_values = ", ".join(
        f"{column} = '{value}'" for column, value in zip(columns, values)
    )
    query = f"UPDATE {table} SET {set_values}"

    if where:
        query += f" WHERE {where}"

    db.execute(query, args)
    db.commit()


def delete(db, table, where, args=()):
    query = f"DELETE FROM {table} WHERE {where}"

    db.execute(query, args)
    db.commit()
