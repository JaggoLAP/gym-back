from src.models.user_model import get_user_by_email
from werkzeug.security import check_password_hash

def authenticate_user(email, password):
    user = get_user_by_email(email)

    if not user:
        
        return None

    if check_password_hash(user["password"], password):

        return user

    return None

