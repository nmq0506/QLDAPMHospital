import math

from flask import render_template, jsonify, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, dao,utils,login
from app.models import *

from flask_login import login_user, logout_user
from fontTools.misc.plistlib import end_date
from sqlalchemy import func
from wtforms.validators import email
from datetime import datetime, timedelta, date, time
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
            return redirect("/doctor/home")
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


@app.route("/")
def index():
    # return render_template("Doctor/home_schedule_doctor.html")
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

@app.route('/doctors/<int:doctor_id>')
def doctor_detail(doctor_id):
    doctor = dao.get_doctor_by_id(doctor_id)

    return render_template("User/doctor_detail.html", doctor=doctor)

@app.route("/admin/table-list-doctor")
def get_doctor():
    return render_template('Admin/list_doctor.html', user = utils.get_doctor());
@app.route("/admin/table-list-user")
def get_user():
    return render_template('Admin/list_user.html', user = utils.get_user());
#Nguyen lm
# @app.route('/appointments-doctor')
@app.route("/schedule-doctor/<int:doctor_id>/<string:date_str>")
# @app.route("/")
def schedule_view(doctor_id,date_str):
    current_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    start_of_week = current_date - timedelta(days=current_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    prev_week_date = start_of_week - timedelta(days=1)
    next_week_date = end_of_week + timedelta(days=1)
    today_date = date.today()

    # Lọc dữ liệu theo doctor_id VÀ tuần
    appointments_doctor = dao.get_appointments_doctor_accept(doctor_id=doctor_id)
    appointments_this_week = [
        appo for appo in appointments_doctor
        if start_of_week <= appo.date.date() <= end_of_week
    ]

    time_slots = [
        "06:30", "06:35", "06:40", "06:45", "06:50", "06:55",
"07:00", "07:05", "07:10", "07:15", "07:20", "07:25", "07:30", "07:35", "07:40", "07:45", "07:50", "07:55",
"08:00", "08:05", "08:10", "08:15", "08:20", "08:25", "08:30", "08:35", "08:40", "08:45", "08:50", "08:55",
"09:00", "09:05", "09:10", "09:15", "09:20", "09:25", "09:30", "09:35", "09:40", "09:45", "09:50", "09:55",
"10:00", "10:05", "10:10", "10:15", "10:20", "10:25", "10:30", "10:35", "10:40", "10:45", "10:50", "10:55",
"11:00", "11:05", "11:10", "11:15",
"13:00", "13:05", "13:10", "13:15", "13:20", "13:25", "13:30", "13:35", "13:40", "13:45", "13:50", "13:55",
"14:00", "14:05", "14:10", "14:15", "14:20", "14:25", "14:30", "14:35", "14:40", "14:45", "14:50", "14:55",
"15:00", "15:05", "15:10", "15:15", "15:20", "15:25", "15:30", "15:35", "15:40", "15:45", "15:50", "15:55",
"16:00", "16:05", "16:10", "16:15", "16:20", "16:25", "16:30", "16:35", "16:40", "16:45", "16:50", "16:55",
"17:00"
    ]
    days = range(2, 9)
    schedule_grid = {}

    for time in time_slots:
        row_of_cells = {}
        for day in days:
            row_of_cells[day] = {'type': 'empty'}
        schedule_grid[time] = row_of_cells



    for appo in appointments_this_week:

        start_datetime = appo.date
        end_datetime = start_datetime + timedelta(hours=0.5)

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

    return render_template(
        'schedule.html',
        doctor_id=doctor_id,
        time_slots=time_slots,
        schedule_grid=schedule_grid,
        start_of_week=start_of_week,
        end_of_week=end_of_week,
        prev_week_date=prev_week_date,
        today_date=today_date,
        next_week_date=next_week_date
    )
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
    specialties = dao.find_all_specialty()
    return render_template('booking_form.html', hospitals=hospitals, specialties=specialties)
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
            booked_by=current_user.id
        )
        dao.create_appointment(new_appointment=new_appointment)



        return render_template("booking_form.html")





@app.route('/get-doctors/<int:hospital_id>/specialty/<int:specialty_id>')
def get_doctors(hospital_id,specialty_id):
    doctors = dao.find_by_hos_id_and_specialties_id_doctor(hospital_id=hospital_id, specialty_id=specialty_id)
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
    time_start= dao.find_by_doctor_id_schedule_doctor(doctor_id)
    time_end_str = "2025-08-20 17:00:00"
    time_end_datetime = datetime.strptime(time_end_str, "%Y-%m-%d %H:%M:%S")


    booked_times = [appointment.date.time() for appointment in booked_appointments]


    potential_slots = []

    current_slot_dt = datetime.combine(selected_date, time_start.schedule_date.time())
    end_time_dt = datetime.combine(selected_date,time_end_datetime.time())

    while current_slot_dt < end_time_dt:
        potential_slots.append(current_slot_dt)
        current_slot_dt += timedelta(minutes=5)

    LUNCH_TIME = {
        time(11, 5), time(11, 10), time(11, 15), time(11, 20), time(11, 25),
        time(11, 30), time(11, 35), time(11, 40), time(11, 45), time(11, 50),
        time(11, 55), time(12, 0), time(12, 5), time(12, 10), time(12, 15),
        time(12, 20), time(12, 25), time(12, 30), time(12, 35), time(12, 40),
        time(12, 45), time(12, 50), time(12, 55),
    }



    available_slots = [ slot for slot in potential_slots if (slot.time() not in booked_times) and (slot.time() not in LUNCH_TIME)
    ]



    available_slots_str = [slot.strftime('%Y-%m-%d %H:%M') for slot in available_slots]

    return jsonify({'schedule': available_slots_str})

@app.route("/home_schedule_doctor")
def home_schedule_doctor():
    appts = dao.get_appointments_doctor_accept(current_user.id)

    event_list=[]

    for appt in appts:
        events = {}
        end_date = appt.date + timedelta(hours=1)
        events['title']=appt.note
        events['start'] = appt.date.isoformat()
        events['end'] = end_date.isoformat()
        event_list.append(events)
    return jsonify({'events': event_list})

@app.route("/list-appt")
def list_appp():
    page = request.args.get('page')
    list_appt= dao.find_appt_join_patient_doctor(current_user.id,page=page)
    return render_template("Doctor/list_appt.html",list_appt=list_appt,pages=math.ceil(dao.count_appt()/3 ))

@app.route("/change-status/<int:appt_id>")
def change_status_cancel(appt_id):
    dao.change_status_cancel(appt_id)
    list_appt = dao.find_appt_join_patient_doctor(current_user.id)
    return render_template("Doctor/list_appt.html",list_appt=list_appt,pages=math.ceil(dao.count_appt()/3 ))
@app.route("/doctor/home")
def home_doctor():
    return render_template("Doctor/home_schedule_doctor.html")

@app.route('/doctors/<int:id>')
def doctor_details(id):
    doctor = dao.get_doctor(doctor_id=id)
    comments = dao.get_comments(doctor_id=id)
    return render_template('User/doctors-details.html', doctor=doctor, comments=comments)

@app.route('/api/doctors/<int:id>/comments', methods=['post'])
@login_required
def add_comment(id):
    data = request.json
    c = dao.add_comment(content=data.get('content'), doctor_id=id)

    return jsonify({'id': c.id, 'content': c.comment, 'user': {
        'username': c.user_review.username,
        'avatar': "https://res-console.cloudinary.com/dieiwsp2i/thumbnails/v1/image/upload/v1749404808/cm5iamdqYW5veXFwbXRxZnlwNjk=/drilldown"
    }})

@app.route("/list-appt-user")
def list_appp_user():
    page = request.args.get('page')
    list_appt= dao.find_appt_join_patient_doctor_booked_by(current_user.id,page=page)
    return render_template("User/list_appt.html",list_appt=list_appt,pages=math.ceil(dao.count_appt()/3 ))

@app.route("/change-status-appt-user/<int:appt_id>")
def change_status_cancel_user(appt_id):
    dao.change_status_cancel(appt_id)
    list_appt = dao.find_appt_join_patient_doctor_booked_by(current_user.id)
    return render_template("User/list_appt.html",list_appt=list_appt,pages=math.ceil(dao.count_appt()/3 ))

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

@app.route("/admin/revenue_weekly")
def revenue_weekly():
    year = request.args.get("year", type=int)
    week = request.args.get("week", type=int)

    # Nếu không truyền thì mặc định là tuần hiện tại
    if not year or not week:
        today = datetime.now()
        iso = today.isocalendar()  # (year, week_number, weekday)
        year, week = iso[0], iso[1]

    result = dao.get_weekly_revenue(year, week)

    # Tính ra ngày đầu tuần (Monday)
    monday = datetime.strptime(f"{year}-W{week}-1", "%G-W%V-%u")

    # Build dữ liệu cho 7 ngày (Mon → Sun)
    data = []
    for i in range(7):
        day = monday + timedelta(days=i)
        found = next((r.total for r in result if r.date == day.date()), 0)
        data.append({"date": day.strftime("%d/%m/%Y"), "total": found})

    return render_template("Admin/revenue_weekly.html", data=data, year=year, week=week)

@app.route("/admin/revenue_monthly")
def revenue_monthly():
    year = request.args.get("year", datetime.now().year, type=int)
    month = request.args.get("month", datetime.now().month, type=int)

    labels, data = dao.get_monthly_revenue(year, month)

    return render_template(
        "Admin/revenue_monthly.html",
        labels=labels,
        data=data,
        selected_year=year,
        selected_month=month
    )

@app.route("/admin/revenue_yearly")
def revenue_yearly():
    year = request.args.get("year", datetime.now().year, type=int)

    labels, data = dao.get_yearly_revenue(year)

    return render_template(
        "Admin/revenue_yearly.html",
        labels=labels,
        data=data,
        selected_year=year
    )

if "__main__" == __name__:
    app.run(debug=True,port=8080)