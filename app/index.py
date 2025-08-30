from flask import render_template, jsonify, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, dao,utils,login
from app.models import *

from flask_login import login_user, logout_user
from sqlalchemy import func
from wtforms.validators import email
from datetime import datetime, timedelta
from app import app, dao,utils,login, db
from app.models import UserRole, Doctor, Patient, AppointmentSchedule,Hospital
@app.route('/user/login', methods=['get', 'post'])
def user_login():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user_role = request.form.get('user_role')
        u = utils.auth_user(username=username, password=password, role=UserRole.USER)
        if u:
            login_user(u)
            return redirect('/')
        else:
            err_msg = "Tai khoan hoac mat khau sai !!!"
    return render_template('User/login.html', err_msg=err_msg)


@app.route('/doctor/login', methods=['get', 'post'])
def doctor_login():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user_role = request.form.get('user_role')
        u = utils.auth_user(username=username, password=password, role=UserRole.DOCTOR)
        if u:
            login_user(u)
            return redirect('/')
        else:
            err_msg = "Tai khoan hoac mat khau sai !!!"
    return render_template('Doctor/login.html', err_msg=err_msg)


@app.route('/admin/login', methods=['get', 'post'])
def admin_login():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user_role = request.form.get('user_role')
        u = utils.auth_user(username=username, password=password, role=UserRole.ADMIN)
        if u:
            login_user(u)
            return redirect('/admin/home')
        else:
            err_msg = "Tai khoan hoac mat khau sai !!!"
    return render_template('Admin/login.html', err_msg=err_msg)


@app.route('/admin/home', methods=['get', 'post'])
def admin_home():
    return render_template('Admin/home.html')


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id)
@app.route("/user/logout")
def user_logout():
    logout_user()
    return redirect('/user/login')


@app.route("/user/register", methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        phone = request.form.get('phone')
        email = request.form.get('email')
        confirm = request.form.get('confirm')

        try:
            if password.strip().__eq__(confirm.strip()):
                utils.add_user(name=name, username=username,
                               password=password,
                               phone=phone,
                               user_role=UserRole.USER,
                               email=email
                               )
                return redirect('/user/login')
            else:
                err_msg = 'MAT KHAU KHONG KHOP !!!'
        except Exception as ex:
            err_msg = "He thong dang co loi: " + str(ex)
    return render_template('User/register.html', err_msg=err_msg)


@app.route("/doctor/register", methods=['get', 'post'])
def doctor_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        phone = request.form.get('phone')
        email = request.form.get('email')
        confirm = request.form.get('confirm')

        try:
            if password.strip().__eq__(confirm.strip()):
                utils.add_doctor(name=name, username=username,
                                 password=password,
                                 phone=phone,
                                 user_role=UserRole.DOCTOR,
                                 email=email

                                 )
                flash("Đăng ký tài khoản bác sĩ thành công!", "success")
                return redirect('/doctor/login')
            else:
                err_msg = 'MAT KHAU KHONG KHOP !!!'
        except Exception as ex:
            err_msg = "He thong dang co loi: " + str(ex)
    return render_template('Admin/doctor_register.html', err_msg=err_msg)


@app.route("/user/logout")
def user_logout():
    logout_user()
    return render_template('User/login.html')


@app.route("/")
def index():
    return render_template("User/home.html")


@app.route('/specialties')
def specialties():
    kw = request.args.get('kw')
    specialties = dao.load_specialties(kw)
    return render_template("User/specialties.html", specialties=specialties, kw=kw)


@app.route('/doctors')
def doctors():
    kw = request.args.get('kw')
    specialty_id = request.args.get('specialty_id')
    hospital_id = request.args.get('hospital_id')
    degree = request.args.get('degree')
    doctors = dao.get_doctors(kw ,specialty_id, hospital_id, degree)
    specialties = dao.load_specialties()
    hospitals = dao.load_hospital()
    return render_template("User/doctors.html", kw=kw, specialty_id=specialty_id,
                           hospital_id=hospital_id, doctors=doctors, degree=degree, specialties=specialties,
                           hospitals=hospitals)

@app.route("/admin/table-list-doctor")
def get_doctor():
    return render_template('Admin/list_doctor.html', user = utils.get_doctor());
@app.route("/admin/table-list-user")
def get_user():
    return render_template('Admin/list_user.html', user = utils.get_user());
#Nguyen lm
# @app.route('/appointments-doctor')
@app.route("/schedule-doctor/<int:doctor_id>")
# @app.route("/")
def schedule_view(doctor_id):

    time_slots = [
        "06:30", "06:45", "07:00", "07:15", "07:30", "07:45", "08:00", "08:15", "08:30", "08:45",
       "09:00", "09:15", "09:30", "09:45", "10:00", "10:15", "10:30", "10:45", "11:00", "12:00", "12:15", "12:30", "12:45", "13:00", "13:15", "13:30", "13:45",
       "14:00", "14:15", "14:30", "14:45", "15:00", "15:15", "15:30", "15:45", "16:00", "16:15",
       "16:30", "16:45", "17:00"
    ]
    days = range(2, 9)
    schedule_grid = {}

    for time in time_slots:
        row_of_cells = {}
        for day in days:
            row_of_cells[day] = {'type': 'empty'}
        schedule_grid[time] = row_of_cells


    appointments_doctor = dao.get_appointments_doctor_accept(doctor_id=doctor_id)
    for appo in appointments_doctor:

        start_datetime = appo.date
        end_datetime = start_datetime + timedelta(hours=1)

        start_str = start_datetime.strftime('%H:%M')
        end_str = end_datetime.strftime('%H:%M')



        start_index = time_slots.index(start_str)
        end_index = time_slots.index(end_str)
        duration = end_index - start_index

        # isoweekday() trả về: T2=1, ..., CN=7. Cộng 1 để khớp với cột (T2=2)
        day_column = start_datetime.isoweekday() + 1


        schedule_grid[start_str][day_column] = {
            'type': 'event',
            'title': appo.note,
            'class': 'event-green',
            'rowspan': duration,
            'start_str' : start_str,
            'end_str' : end_str
        }


        for i in range(1, duration):
            time_to_mark = time_slots[start_index + i]
            schedule_grid[time_to_mark][day_column] = {'type': 'spanned'}


    return render_template('schedule.html', time_slots=time_slots, schedule_grid=schedule_grid)
# @app.route("/")
def chat():
    return render_template("chat.html")
@app.route("/accept/<int:appointment_id>", methods=["POST"])
def update_accept_doctor(appointment_id):
    dao.update_appointment_doctor(appointment_id=appointment_id)
    return redirect("/")
#--------------------------
@app.route("/booking")
def form_booking():
    hospitals = dao.find_all_hospital()
    return render_template('booking_form.html', hospitals=hospitals)
@app.route('/book-appointment', methods=['GET', 'POST'])
def book_appointment():

    if request.method == 'POST':

        hospital_id = request.form.get('app')
        doctor_id = request.form.get('doctor')
        patient_name = request.form.get('patient_name')
        selected_time_str = request.form.get('selected_time')  # e.g., "2025-08-10 10:00"
        symptoms = request.form.get('symptoms')


        patient = dao.find_by_name_patient(name=patient_name)

        if patient:

            print(f"Bệnh nhân '{patient_name}' đã tồn tại. Sử dụng ID: {patient.id}")
            patient_id = patient.id
        else:

            print(f"Bệnh nhân '{patient_name}' chưa có. Tạo mới...")
            new_patient = Patient(name=patient_name, age=0)
            db.session.add(new_patient)
            db.session.flush()
            patient_id = new_patient.id


        appointment_date = datetime.strptime(selected_time_str, '%Y-%m-%d %H:%M')

        new_appointment = AppointmentSchedule(
            doctor_id=doctor_id,
            patient_id=patient.id,
            date=appointment_date,
            note=symptoms,
            room="101",
            booked_by=1
        )
        dao.create_appointment(new_appointment=new_appointment)


        return redirect(url_for('some_confirmation_page'))





@app.route('/get-doctors/<int:hospital_id>')
def get_doctors(hospital_id):
    doctors = dao.find_by_hospital_id_doctor(hospital_id=hospital_id)
    doctor_list = [{'id': doc.id, 'name': doc.name} for doc in doctors]
    return jsonify({'doctors': doctor_list})


@app.route('/get-schedule/<int:doctor_id>')
def get_schedule(doctor_id):

    selected_date_str = request.args.get('date')
    if not selected_date_str:
        return jsonify({'error': 'A date must be provided'}), 400

    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    doctor = dao.find_by_id_doctoc(doctor_id=doctor_id)
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404


    booked_appointments = dao.find_by_doctor_id_and_date_appointment(doctor_id, selected_date)


    booked_times = [appointment.date.time() for appointment in booked_appointments]


    potential_slots = []

    current_slot_dt = datetime.combine(selected_date, doctor.time_start.time())
    end_time_dt = datetime.combine(selected_date, doctor.time_end.time())

    while current_slot_dt < end_time_dt:
        potential_slots.append(current_slot_dt)
        current_slot_dt += timedelta(hours=1)


    available_slots = [
        slot for slot in potential_slots if slot.time() not in booked_times
    ]


    available_slots_str = [slot.strftime('%Y-%m-%d %H:%M') for slot in available_slots]

    return jsonify({'schedule': available_slots_str})


@app.route('/patient_records', methods=['GET'])
@login_required
def patient_records():
    if current_user.user_role != UserRole.DOCTOR:
        flash("Bạn không có quyền truy cập", "danger")
        return redirect(url_for('index'))

    doctor_id = current_user.id
    patient_profiles = (
        db.session.query(
            AppointmentSchedule.id.label("appointment_id"),
            Patient.name.label("patient_name"),
            Patient.age,
            Patient.email,
            Patient.phone,
            AppointmentSchedule.status.label("appointment_status")
        )
        .join(Patient, AppointmentSchedule.patient_id == Patient.id)
        .filter(AppointmentSchedule.doctor_id == doctor_id)
        .all()
    )

    return render_template(
        'Doctor/patient_records.html',
        patient_profiles=patient_profiles
    )

@app.route('/patient_records/<int:appointment_id>', methods=['GET'])
@login_required
def patient_record_detail(appointment_id):
    if current_user.user_role != UserRole.DOCTOR:
        flash("Bạn không có quyền truy cập", "danger")
        return redirect(url_for('index'))

    doctor_id = current_user.id
    record = (
        db.session.query(
            AppointmentSchedule.id.label("appointment_id"),
            Patient.name.label("patient_name"),
            Patient.age,
            Patient.phone,
            Patient.email,
            ProfilePatient.symptom,
            ProfilePatient.diagnose,
            ProfilePatient.test_result,
            ProfilePatient.medical_history
        )
        .join(Patient, AppointmentSchedule.patient_id == Patient.id)
        .outerjoin(ProfilePatient, ProfilePatient.patient_id == Patient.id)
        .filter(AppointmentSchedule.id == appointment_id)
        .filter(AppointmentSchedule.doctor_id == doctor_id)
        .first()
    )

    if not record:
        flash("Không tìm thấy hồ sơ hoặc bạn không có quyền", "warning")
        return redirect(url_for('patient_records'))

    return render_template('Doctor/patient_record_detail.html', record=record)

if "__main__" == __name__:
    app.run(debug=True,port=8080)