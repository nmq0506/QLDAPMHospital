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




class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    avatar = Column(String(100))
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

class Doctor(db.Model):
    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    name = Column(String(50), nullable=False)
    certificate = Column(String(50), nullable=False)
    specialty = Column(String(50), nullable=False)
    experience_years = Column(Integer,nullable=False)
    time_start = Column(DateTime, nullable=False)
    time_end = Column(DateTime, nullable=False)
    hospital_id = Column(Integer, ForeignKey(Hospital.id),nullable=False)
    appointments = relationship('AppointmentSchedule', backref='doctor', lazy=True)
    reviews = relationship('Review', backref='doctor', lazy=True)

    def __str__(self):
        return self.name

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
        db.create_all()
        # u = User(name='Quân', username='mq', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),phone='0123456789',email='123@gmail.com',
        #          user_role=UserRole.USER)
        # db.session.add(u)
        # db.session.commit()