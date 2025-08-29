from app.models import User
from app import db


def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_email_password(email, password):
    return User.query.filter_by(email=email, password=password).first()

def get_all_users():
    return User.query.all()

def user_exists(email):
    return User.query.filter_by(email=email).first() is not None

def create_new_user(first_name, last_name, email, password):
    user = User(first_name=first_name, last_name=last_name, email=email, password=password, type='user')
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def update_user_by_admin(user_id, first_name, last_name, email, password):
    user = User.query.get(user_id)
    if user:
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.password = password
        db.session.commit()
    return user

def delete_user(user_id):
    """מחיקת משתמש לפי ID"""
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False