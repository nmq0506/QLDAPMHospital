import datetime
import hashlib
from app.models import User,UserRole
from app import app, db
from datetime import datetime, timedelta

def get_user_by_id(id):
    return User.query.get(id)
def auth_user(username, password, role=UserRole.USER):
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password),
                            User.user_role.__eq__(role)).first()
def add_user(name, username, password, user_role,phone,email, **kwargs):
    user = User(name=name,
                username=username,
                password=str(hashlib.md5(password.strip().encode('utf-8')).hexdigest()),

                user_role=UserRole.USER,
                phone= phone,
                email=email
                )
    db.session.add(user)
    db.session.commit()

def add_doctor(name, username, password, user_role,phone,email, **kwargs):
    user = User(name=name,
                username=username,
                password=str(hashlib.md5(password.strip().encode('utf-8')).hexdigest()),
                user_role=UserRole.DOCTOR,
                phone= phone,
                email=email
                )
    db.session.add(user)
    db.session.commit()