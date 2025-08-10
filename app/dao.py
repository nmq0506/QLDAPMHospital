import data,json
from sqlalchemy.orm import joinedload
from app.models import Specialty, Doctor, Hospital, User


def load_specialties(kw=None):
    query = Specialty.query

    if kw:
        query = query.filter(Specialty.name.ilike(f"%{kw}%"))

    return query.all()

def get_doctors(kw=None, spec_id=None, hospital_id=None, degree=None):
    query = Doctor.query.join(Doctor.user)  # join với User để truy cập name

    if kw:
        query = query.filter(User.name.ilike(f"%{kw}%"))
    if spec_id:
        query = query.filter(Doctor.specialty_id == spec_id)
    if hospital_id:
        query = query.filter(Doctor.hospital_id == hospital_id)
    if degree:
        query = query.filter(Doctor.certificate == degree)

    return query.options(joinedload(Doctor.user)).all()

def load_hospital():
    return Hospital.query.all()


def auth_user(username, password):
    with open("data/data.json", encoding="utf-8") as f:
        users= json.load(f)
        for u in users:
            if u["username"]==username and u["password"]== password:
                return True
    return False