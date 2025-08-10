import data,json
from app.models import Specialty, Doctor, Hospital


def load_specialties(kw=None):
    query = Specialty.query

    if kw:
        query = query.filter(Specialty.name.ilike(f"%{kw}%"))

    return query.all()

def get_doctors(kw=None, spec_id=None, hospital_id=None, degree=None):
    query = Doctor.query
    if kw:
        query = query.filter(Doctor.name.ilike(f"%{kw}%"))
    if spec_id:
        query = query.filter(Doctor.specialty_id==spec_id)
    if hospital_id:
        query = query.filter(Doctor.hospital_id==hospital_id)
    if degree:
        query = query.filter(Doctor.certificate==degree)
    return query.all()

def get_doctor_by_id(doctor_id):
    return Doctor.query.get(doctor_id)

def load_hospital():
    return Hospital.query.all()


def auth_user(username, password):
    with open("data/data.json", encoding="utf-8") as f:
        users= json.load(f)
        for u in users:
            if u["username"]==username and u["password"]== password:
                return True
    return False