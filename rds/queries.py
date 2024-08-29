def get_user(conn, name):
    err_string = None

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mybackdatabase.users WHERE username = %(name)s", {'name': name})
    row = cursor.fetchone()

    if row is None:
        err_string = f"Name '{name}' not found"
        return None, err_string

    # Get the column names
    column_names = [desc[0] for desc in cursor.description]

    # Combine column names with row data into a dictionary
    row_with_titles = dict(zip(column_names, row))

    return row_with_titles, err_string
