def handle_post(db, form):
    try:
        db.execute(
            "INSERT INTO node (type) VALUES (?)",
            (form.get("type"),),
        )
        db.commit()

        return db.execute("SELECT last_insert_rowid()").fetchone()[0]
    except db.Error as e:
        print(e)


def handle_patch(db, form, id):
    print(id)
    try:
        db.execute(
            "UPDATE node SET active = ? WHERE node_id = ?",
            (form.get("active"), id),
        )
        db.commit()
    except db.Error as e:
        print(e)


def handle_delete(db, form, id):
    pass
