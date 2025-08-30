import datetime
import hashlib
from app.models import User, UserRole, Doctor, Specialty
from app import app, db

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
def get_doctor():
    return db.session.query(User.name, User.username, User.password, User.phone,User.email,User.created_date,Doctor.description,Doctor.certificate,Specialty.name,Doctor.experience_years).join(Doctor, User.id == Doctor.id).join(Specialty, Doctor.specialty_id == Specialty.id).filter(User.user_role=='DOCTOR').all()
def get_user():
    return db.session.query(User.name, User.username, User.password, User.phone,User.email,User.created_date).filter(User.user_role=='USER').all()