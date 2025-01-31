from flask import current_app

def get_user_by_email(email):
    query = "SELECT id, email, password FROM socios WHERE email = %s"

    result = current_app.db.execute_query(query, (email,))


    return result[0] if result else None
