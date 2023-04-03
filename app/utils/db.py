def select(db, table, columns, where=None, order_by=None, limit=None):
    query = f"SELECT {', '.join(columns)} FROM {table}"
    if where:
        query += f" WHERE {where}"
    if order_by:
        query += f" ORDER BY {order_by}"
    if limit:
        query += f" LIMIT {limit}"

    rows = []
    try:
        rows = db.execute(query).fetchall()
    except db.Error as e:
        print(e)

    rows = [dict(row) for row in rows]

    return rows