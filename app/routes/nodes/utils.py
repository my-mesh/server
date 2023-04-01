def handle_json(db, request):
    data = request.json

    try:
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            "INSERT INTO node (type, mesh_id) VALUES (?, ?)",
            ("Test", data["mesh_id"]),
        )
        db.commit()
    except db.Error as e:
        print(e)


def handle_form(db, request):
    print(request.form)


def handle_form_patch(db, request):
    print(request.form)