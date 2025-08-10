from flask import render_template, jsonify, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, dao,utils,login
from app.models import *
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