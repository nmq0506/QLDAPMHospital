from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum, DateTime, Double
from sqlalchemy.orm import relationship, backref
from wtforms.validators import email

from app import db, app
from flask_login import UserMixin
from enum import Enum as PyEnum
from datetime import datetime
import hashlib

class UserRole(PyEnum):
    ADMIN = 1
    USER = 2
    DOCTOR= 3

class AppointmentScheduleStatus(PyEnum):
    ACCEPT = 1
    PENDING = 2
    CANCEL = 3

class PaymentStatus(PyEnum):
    PENDING = 1
    SUCCESS = 2
    FAILED = 3

class CertificateEnum(PyEnum):
    PGS_TS = 'PGS.TS'
    TS = 'TS'
    THS = 'ThS'
    BS_CKII = 'BS.CKII'
    BS_CKI = 'BS.CKI'


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    created_date = Column(DateTime, default=datetime.now())
    doctor_profile = relationship("Doctor",backref=backref("user", uselist=False), uselist=False) # 1-1
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    appointments = relationship('AppointmentSchedule', backref='user', lazy=True)
    reviews = relationship('Review', backref='user_review', lazy=True)

    def __str__(self):
        return self.name


class Hospital(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    location = Column(String(50), nullable=False)
    doctors = relationship('Doctor', backref= 'hospital', lazy=True)


    def __str__(self):
        return self.name

class Specialty(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    image = Column(String(255), nullable=False)
    doctors = relationship('Doctor', backref='specialty', lazy=True)

    def __str__(self):
        return self.name

class Doctor(db.Model):
    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    avatar = Column(String(100))
    description = Column(String(255), nullable=False)
    certificate = Column(Enum(CertificateEnum), default=CertificateEnum.THS)
    specialty_id = Column(Integer, ForeignKey(Specialty.id), nullable=False)
    experience_years = Column(Integer,nullable=False)
    hospital_id = Column(Integer, ForeignKey(Hospital.id),nullable=False)
    appointments = relationship('AppointmentSchedule', backref='doctor', lazy=True)
    reviews = relationship('Review', backref='doctor', lazy=True)
    # schedules = relationship('DoctorSchedule', backref='doctor', lazy=True)

    @property
    def name(self):
        return self.user.name if self.user else None

class DoctorSchedule:
    id = Column(Integer, primary_key=True, autoincrement=True)
    schedule_date = Column(DateTime, default=datetime.now())
    doctor_id = Column(Integer, ForeignKey(Doctor.id), nullable=False)

class Review(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    comment = Column(String(100), nullable=False)
    star = Column(Double,nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer,ForeignKey(User.id), nullable=False)
    doctor_id = Column(Integer,ForeignKey(Doctor.id),nullable=False)

class Patient(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    phone = Column(String(50), nullable=True)
    email = Column(String(50), nullable=True)
    profilePatients = relationship('ProfilePatient', backref='patient_pro', lazy=True)
    appointments = relationship('AppointmentSchedule', backref='patient', lazy=True)

class ProfilePatient(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    symptom = Column(String(100), nullable=False)
    diagnose = Column(String(100), nullable=False)
    test_result = Column(String(100), nullable=False)
    medical_history = Column(String(100), nullable=False)
    patient_id = Column(Integer,ForeignKey(Patient.id),nullable=False)
    created_date = Column(DateTime, default=datetime.now())

class AppointmentSchedule(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    room = Column(String(50), nullable=False)
    date = Column(DateTime)
    created_date = Column(DateTime, default=datetime.now())
    status = Column(Enum(AppointmentScheduleStatus), default=AppointmentScheduleStatus.PENDING)
    note = Column(String(100),nullable=True)
    doctor_id = Column(Integer, ForeignKey(Doctor.id), nullable=False)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)
    booked_by = Column(Integer, ForeignKey(User.id), nullable=False)
    payment = relationship("Payment", backref=backref("appointment", uselist=False), uselist=False)



class Payment(db.Model):
    id = Column(Integer, ForeignKey(AppointmentSchedule.id),primary_key=True)
    total_price = Column(Integer)
    created_date = Column(DateTime, default=datetime.now())
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)

if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        # u = User(name='Quân', username='mq', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),phone='0123456789',email='123@gmail.com',
        #          user_role=UserRole.USER)
        # db.session.add(u)
        # db.session.commit()
        # specialties = [{
        #     'name': 'Khoa nhi',
        #     'image': 'https://res.cloudinary.com/ds4oggqzq/image/upload/v1753479547/khoa_ngo%E1%BA%A1i_nhi_smutnx.png'
        # }, {
        #     'name': 'Khoa sản phụ',
        #     'image': 'https://res.cloudinary.com/ds4oggqzq/image/upload/v1753479547/Khoa_s%E1%BA%A3n_al9enx.png'
        # }, {
        #     'name': 'Khoa mắt',
        #     'image': 'https://res.cloudinary.com/ds4oggqzq/image/upload/v1753479554/khoa_m%E1%BA%AFt_lgnxch.png'
        # }, {
        #     'name': 'Khoa y học cổ truyền',
        #     'image': 'https://res.cloudinary.com/ds4oggqzq/image/upload/v1753479548/Khoa_y_h%E1%BB%8Dc_c%E1%BB%95_truy%E1%BB%81n_cc59bi.png'
        # }, {
        #     'name': 'Khoa tim mạch',
        #     'image': 'https://res.cloudinary.com/ds4oggqzq/image/upload/v1753479547/khoa_tim_m%E1%BA%A1ch_e4fgfk.png'
        # }, {
        #     'name': 'Khoa da liễu',
        #     'image': 'https://res.cloudinary.com/ds4oggqzq/image/upload/v1753479547/da_li%E1%BB%85u_dfp3rc.png'
        # }, {
        #     'name': 'Khoa răng hàm mặt',
        #     'image': 'https://res.cloudinary.com/ds4oggqzq/image/upload/v1753479548/r%C4%83ng_h%C3%A0m_m%E1%BA%B7t_soy0of.png'
        # }, {
        #     'name': 'Khoa tâm thần',
        #     'image': 'https://res.cloudinary.com/ds4oggqzq/image/upload/v1753479549/th%E1%BA%A7n_kinh_ucks8c.png'
        # }, {
        #     'name': 'Khoa ngoại tổng hợp',
        #     'image': 'https://res.cloudinary.com/ds4oggqzq/image/upload/v1753479548/khoa_ngo%E1%BA%A1i_t%E1%BB%95ng_h%E1%BB%A3p_qa7ufy.png'
        # }]
        # for s in specialties:
        #     specialty = Specialty(**s)
        #     db.session.add(specialty)
        # db.session.commit()
        #
        # hospitals = [{
        #     'name': 'Bệnh viện Tâm Anh',
        #     'location': 'Q8'
        # }, {
        #     'name': 'Bệnh viện Chợ rẫy',
        #     'location': 'Q5'
        # }, {
        #     'name': 'Bệnh viện Quân Y 175',
        #     'location': 'GV'
        # }, {
        #     'name': 'Bệnh viện CTCH TPHCM',
        #     'location': 'Q1'
        # }, {
        #     'name': 'Bệnh viện Bạch Mai',
        #     'location': 'HN'
        # }]
        # for h in hospitals:
        #     hospitals = Hospital(**h)
        #     db.session.add(hospitals)
        # db.session.commit()
        # users = [{
        #     'name': 'Lê Tấn Sơn',
        #     'username': 'sonlt',
        #     'password': hashlib.md5('123456'.encode('utf-8')).hexdigest(),
        #     'phone': '0123452',
        #     'email': '12223@gmail.com',
        #     'user_role': 'doctor'
        # }, {
        #     'name': 'Nguyễn Đức Tuấn',
        #     'username': 'tuannd',
        #     'password': hashlib.md5('123456'.encode('utf-8')).hexdigest(),
        #     'phone': '0123452222',
        #     'email': '1223@gmail.com',
        #     'user_role': 'doctor'
        # }, {
        #     'name': 'Đỗ Ngọc Lâm',
        #     'username': 'lamdn',
        #     'password': hashlib.md5('123456'.encode('utf-8')).hexdigest(),
        #     'phone': '0123452456',
        #     'email': '12222133@gmail.com',
        #     'user_role': 'doctor'
        # }, {
        #     'name': 'Phạm Thị Loan',
        #     'username': 'loanpt',
        #     'password': hashlib.md5('123456'.encode('utf-8')).hexdigest(),
        #     'phone': '0123459',
        #     'email': '1223a@gmail.com',
        #     'user_role': 'doctor'
        # }, {
        #     'name': 'Cam Ngọc Phượng',
        #     'username': 'phuongcn',
        #     'password': hashlib.md5('123456'.encode('utf-8')).hexdigest(),
        #     'phone': '012312459',
        #     'email': '122aaa3a@gmail.com',
        #     'user_role': 'doctor'
        # }]
        # for u in users:
        #     user = User(**u)
        #     db.session.add(user)
        # db.session.commit()

        doctors = [{
            'id': 2,
            'avatar': 'https://res.cloudinary.com/ds4oggqzq/image/upload/v1753538716/sonlt_g7xedr.jpg',
            'certificate': CertificateEnum.PGS_TS,
            'specialty_id': 1,
            'hospital_id': 1,
            'experience_years': 20,
            'description': 'Cố vấn chuyên môn Khoa Ngoại Nhi'
        }, {
            'id': 3,
            'avatar': 'https://res.cloudinary.com/ds4oggqzq/image/upload/v1753540213/tuannd_ynmsle.jpg',
            'certificate': CertificateEnum.PGS_TS,
            'specialty_id': 2,
            'hospital_id': 1,
            'experience_years': 11,
            'description': 'Chuyên viên khoa sản phụ'
        }, {
            'id': 4 ,
            'avatar': 'https://res.cloudinary.com/ds4oggqzq/image/upload/v1753583209/dr3jpg_gil8fr.jpg',
            'certificate': CertificateEnum.BS_CKII,
            'specialty_id': 1,
            'hospital_id': 2,
            'experience_years': 20,
            'description': 'Bác sĩ chuyên môn Khoa Ngoại Nhi'
        }, {
            'id': 5,
            'avatar': 'https://res.cloudinary.com/ds4oggqzq/image/upload/v1753583244/dr4_txdd7q.jpg',
            'certificate': CertificateEnum.THS,
            'specialty_id': 4,
            'hospital_id': 3,
            'experience_years': 11,
            'description': 'Chuyên viên bệnh viện'
        }, {
            'id': 6,
            'avatar': 'https://res.cloudinary.com/ds4oggqzq/image/upload/v1753583379/dr5_mdrqri.jpg',
            'certificate': CertificateEnum.TS,
            'specialty_id': 2,
            'hospital_id': 1,
            'experience_years': 11,
            'description': 'Giám đốc Trung tâm Sơ sinh Bệnh viện Đa khoa Tâm Anh TP.HCM'
        }]

        for doctor in doctors:
            doctor = Doctor(**doctor)
            db.session.add(doctor)
        db.session.commit()