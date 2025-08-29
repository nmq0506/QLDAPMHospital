# import data,json
from app.models import Specialty, Doctor, Hospital, AppointmentSchedule, AppointmentScheduleStatus, Patient, \
    DoctorSchedule, Review
from sqlalchemy import or_, func
from flask_login import current_user
from sqlalchemy.orm import joinedload
from app import db
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

def load_hospital():
    return Hospital.query.all()


# def auth_user(username, password):
#     with open("data/data.json", encoding="utf-8") as f:
#         users= json.load(f)
#         for u in users:
#             if u["username"]==username and u["password"]== password:
#                 return True
#     return False

def add_appointment():
    a = AppointmentSchedule()
    db.session.add(a)
    db.session.commit()

def get_appointments_doctor_pending(doctor_id):
    # return AppointmentSchedule.query \
    #     .options(joinedload(AppointmentSchedule.patient),
    #              joinedload(AppointmentSchedule.doctor)) \
    #     .filter(
    #     AppointmentSchedule.doctor_id.__eq__(doctor_id),
    #     AppointmentSchedule.status.__eq__(AppointmentScheduleStatus.PENDING)
    # ).all()
    return AppointmentSchedule.query.filter(
        AppointmentSchedule.doctor_id.__eq__(doctor_id),
        AppointmentSchedule.status.__eq__(AppointmentScheduleStatus.PENDING)
    ).all()

def get_appointments_doctor_accept(doctor_id):
    # return AppointmentSchedule.query \
    #     .options(joinedload(AppointmentSchedule.patient),
    #              joinedload(AppointmentSchedule.doctor)) \
    #     .filter(
    #     AppointmentSchedule.doctor_id.__eq__(doctor_id),
    #     AppointmentSchedule.status.__eq__(AppointmentScheduleStatus.PENDING)
    # ).all()
    return AppointmentSchedule.query.filter(
        AppointmentSchedule.doctor_id.__eq__(doctor_id),
        AppointmentSchedule.status.__eq__(AppointmentScheduleStatus.ACCEPT)
    ).all()

def get_appointments_user(booked_by):
    return AppointmentSchedule.query.filter(
        AppointmentSchedule.doctor_id.__eq__(booked_by)).all()

def update_appointment_doctor(appointment_id):
    c = AppointmentSchedule.query.get(appointment_id)
    c.status = AppointmentScheduleStatus.ACCEPT
    db.session.commit()

def find_by_name_patient(name):
    return Patient.query.filter(Patient.name.__eq__(name)).first()
def find_by_id_doctoc(doctor_id):
    return Doctor.query.get(doctor_id)
def find_by_hospital_id_doctor(hospital_id):
    return Doctor.query.filter(hospital_id==hospital_id).all()
def find_all_hospital():
    return Hospital.query.all()
# Sử dụng func.date() để chỉ so sánh phần ngày của cột 'date' (là kiểu DateTime)
def find_by_doctor_id_and_date_appointment(doctor_id, selected_date):
    return AppointmentSchedule.query.filter(AppointmentSchedule.doctor_id.__eq__(doctor_id),
                                            func.date(AppointmentSchedule.date) == selected_date).all()

def create_appointment(new_appointment):
    db.session.add(new_appointment)
    db.session.commit()





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


# def auth_user(username, password):
#     with open("data/data.json", encoding="utf-8") as f:
#         users= json.load(f)
#         for u in users:
#             if u["username"]==username and u["password"]== password:
#                 return True
#     return False

def find_by_doctor_id_schedule_doctor(doctor_id):
    return DoctorSchedule.query.filter(DoctorSchedule.doctor_id.__eq__(doctor_id)).first()

def find_by_hos_id_and_specialties_id_doctor(hospital_id, specialty_id):
    return Doctor.query.filter(Doctor.hospital_id.__eq__(hospital_id),Doctor.specialty_id.__eq__(specialty_id)).all()

def find_all_specialty():
    return Specialty.query.all()

def find_appt_join_patient_doctor(doctor_id, page=None):
    query= AppointmentSchedule.query \
    .options(joinedload(AppointmentSchedule.patient),
             joinedload(AppointmentSchedule.doctor)) \
    .filter(
    AppointmentSchedule.doctor_id.__eq__(doctor_id),
    AppointmentSchedule.status.__eq__(AppointmentScheduleStatus.ACCEPT))

    if page:
        page_size = 3
        start = (int(page) - 1) * page_size
        query = query.slice(start, start + page_size)

    return query.all()

def change_status_cancel(appt_id):
    a= AppointmentSchedule.query.filter(AppointmentSchedule.id.__eq__(appt_id)).first()
    a.status = AppointmentScheduleStatus.CANCEL
    db.session.commit()

def count_appt():
    return AppointmentSchedule.query.count()

def get_doctor(doctor_id):
    return Doctor.query \
        .options(joinedload(Doctor.hospital),
                 joinedload(Doctor.specialty)) \
        .filter(
        Doctor.id.__eq__(doctor_id)
    ).first()
def get_comments(doctor_id):
    return Review.query.filter(Review.doctor_id.__eq__(doctor_id)).order_by(-Review.id)


def add_comment(content, doctor_id):
    c = Review(comment=content, doctor_id=doctor_id, user_review=current_user,star=5)
    db.session.add(c)
    db.session.commit()

    return c