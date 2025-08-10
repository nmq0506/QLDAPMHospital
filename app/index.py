from flask import render_template, jsonify, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user, login_required

from flask_login import login_user, logout_user
from wtforms.validators import email

from app import app, dao, utils, login
from app.models import UserRole


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
    doctors = dao.get_doctors(kw, specialty_id, hospital_id, degree)
    specialties = dao.load_specialties()
    hospitals = dao.load_hospital()
    return render_template("User/doctors.html", kw=kw, specialty_id=specialty_id,
                           hospital_id=hospital_id, doctors=doctors, degree=degree, specialties=specialties,
                           hospitals=hospitals)


if "__main__" == __name__:
    app.run(debug=True, port=8080)
