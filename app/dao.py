# import data,json
from app.models import Specialty, Doctor, Hospital, AppointmentSchedule, AppointmentScheduleStatus, Patient
from sqlalchemy import or_, func
from app.models import Specialty, Doctor, Hospital, AppointmentSchedule, AppointmentScheduleStatus, Patient, Payment, PaymentStatus
from sqlalchemy import or_, func, extract
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
#     return False

def get_weekly_revenue(year=None, week=None):
    return (
        db.session.query(
            func.date(Payment.created_date).label("date"),
            func.sum(Payment.total_price).label("total")
        )
        .filter(
            extract("year", Payment.created_date) == year,
            func.week(Payment.created_date, 1) == week,  # mode=1: tuần bắt đầu từ Monday
            Payment.status == PaymentStatus.SUCCESS
        )
        .group_by(func.date(Payment.created_date))
        .order_by(func.date(Payment.created_date))
        .all()
    )

def get_monthly_revenue(year, month):
    results = (
        db.session.query(
            func.week(Payment.created_date, 1).label("week"),  # mode 1: tuần bắt đầu từ Monday
            func.sum(Payment.total_price).label("total")
        )
        .filter(
            extract("year", Payment.created_date) == year,
            extract("month", Payment.created_date) == month,
            Payment.status == PaymentStatus.SUCCESS
        )
        .group_by(func.week(Payment.created_date, 1))
        .order_by(func.week(Payment.created_date, 1))
        .all()
    )

    # Trả ra labels và data cho ChartJS
    labels = [f"Tuần {row.week}" for row in results]
    data = [row.total for row in results]
    return labels, data

def get_yearly_revenue(year):
    results = (
        db.session.query(
            extract("month", Payment.created_date).label("month"),
            func.sum(Payment.total_price).label("total")
        )
        .filter(
            extract("year", Payment.created_date) == year,
            Payment.status == PaymentStatus.SUCCESS
        )
        .group_by(extract("month", Payment.created_date))
        .order_by(extract("month", Payment.created_date))
        .all()
    )

    # Sinh đủ 12 tháng (tháng nào không có thì set 0)
    revenue_by_month = {m: 0 for m in range(1, 13)}
    for row in results:
        revenue_by_month[int(row.month)] = row.total

    labels = [f"Tháng {m}" for m in range(1, 13)]
    data = [revenue_by_month[m] for m in range(1, 13)]
    return labels, data
