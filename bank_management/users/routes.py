from flask import (
    render_template,
    url_for, flash,
    redirect,
    request,
    Blueprint,
    abort)
from flask_login import login_user, current_user, logout_user, login_required
from bank_management import db, bcrypt
from bank_management.models import User
from bank_management.users.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    RequestResetForm,
    ResetPasswordForm,
    AdminLoginForm,
    SearchUser,
    DeleteUser)
from bank_management.users.utils import save_picture
from random import randint

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')

        while(1):
            user_crn = randint(10000, 99999)
            crn_user = User.query.filter_by(crn=user_crn).first()
            if not(crn_user):
                break
        if form.picture.data:
            picture_file = save_picture(form.picture.data, user_crn)
            print('data')
            image_file = picture_file
        else:
            image_file = 'default.jpg'
        user = User(
            image_file=image_file,
            first_name=form.first_name.data.upper(),
            crn=user_crn,
            email=form.email.data.lower(),
            password=hashed_password,
            last_name=form.last_name.data.upper(),
            address=form.address.data.upper(),
            pan_number=form.pan_number.data.upper(),
            adhar_number=form.adhar_number.data)

        db.session.add(user)
        db.session.commit()
#        send_new_user_email(user)
        flash(
            'Your account has been created! You are now able to log in'
            'Your crn is ' + str(user_crn),
            'success')
        login_user(user)
        return redirect(url_for('main.home'))

    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return render_template('login.html')


@users.route("/login/userLogin", methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            abort(403)
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(crn=form.crn.data).first()
        if (
                user and bcrypt.check_password_hash(
                    user.password, form.password.data)):

            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            return (
                redirect(next_page)
                if next_page
                else redirect(url_for('main.home')))
        else:
            flash(
                'Login Unsuccessful. Please check CRN and password',
                'danger')
    return render_template('user_login.html', title='Login', form=form)


@users.route("/login/adminLogin", methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        if current_user.is_admin is False:
            abort(403)
        return redirect(url_for('main.home'))
    admin_form = AdminLoginForm()
    if admin_form.validate_on_submit():
        user = User.query.filter_by(email=admin_form.email.data).first()

        if (
            user and bcrypt.check_password_hash(
                user.password,
                admin_form.password.data) and user.is_admin):
            login_user(user, remember=admin_form.remember.data)
            next_page = request.args.get('next')
            return (
                redirect(next_page)
                if next_page
                else redirect(url_for('main.home')))
        else:
            flash(
                'Login Unsuccessful. Please check email and password',
                'danger')
    return render_template(
        'admin_login.html',
        title='Login',
        admin_form=admin_form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(email=form.email.data).first()
        # send_reset_email(user)
        flash(
            'An email has been sent with instructions'
            'to reset your password.',
            'info')
        return redirect(url_for('users.login'))
    return render_template(
        'reset_request.html',
        title='Reset Password',
        form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(
            'Your password has been updated! You are now'
            'able to log in',
            'success')
        return redirect(url_for('users.login'))
    return render_template(
        'reset_token.html',
        title='Reset Password',
        form=form)


@users.route("/delete/user", methods=['GET', 'POST'])
@login_required
def remove_user():
    # if current_user.is_admin is False:
    #     abort(403)
    user_form = SearchUser()
    form = DeleteUser()
    if user_form.user_submit.data and user_form.validate_on_submit():

        user_number = user_form.user_crn.data
        user = User.query.filter_by(crn=user_number).first()
        if user:
            form.account_holder_name.data = (
                user.first_name +
                '  ' +
                user.last_name)
            form.account_holder_crn.data = user.crn
        else:
            flash('Check user CRN', 'danger')
    if form.delete_submit.data and form.validate_on_submit():
        user_crn = form.account_holder_crn.data
        user = User.query.filter_by(crn=user_crn).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            flash('User deleted successfully', 'success')
            return redirect(url_for('user.remove_user'))

    return render_template(
        'delete_user.html',
        title='Delete User',
        form=form,
        user_form=user_form,
        legend='Delete User',
        user_legend='Search User')


@users.route("/update", methods=['GET', 'POST'])
@login_required
def update_info():
    if current_user.is_admin is False:
        abort(403)
    form = UpdateAccountForm()
    user_form = SearchUser()
    if user_form.user_submit.data and user_form.validate_on_submit():
        user_number = user_form.user_crn.data
        user = User.query.filter_by(crn=user_number).first()
        if user:
            form.first_name.data = user.first_name
            form.last_name.data = user.last_name
            form.address.data = user.address
            form.adhar_number.data = user.adhar_number
            form.pan_number.data = user.pan_number
            form.email.data = user.email
            form.picture.data = user.image_file
            form.user_crn.data = user.crn

        else:
            flash('check CRN please', 'danger')
    if form.submit.data and form.validate_on_submit():
        adhar_user = User.query.filter_by(adhar_number=form.adhar_number.data)\
            .filter(User.crn != form.user_crn.data).first()
        pan_user = User.query.filter_by(pan_number=form.pan_number.data)\
            .filter(User.crn != form.user_crn.data).first()
        email_user = User.query.filter_by(email=form.email.data)\
            .filter(User.crn != form.user_crn.data).first()
        if adhar_user or pan_user or email_user:
            flash('Check the updating details', 'danger')
        else:
            user_crn = form.user_crn.data
            user = User.query.filter_by(crn=user_crn).first()
            if user:
                if form.picture.data:
                    picture_file = save_picture(form.picture.data, user_crn)
                    print('data')
                    user.image_file = picture_file
                else:
                    user.image_file = 'default.jpg'
                    print('no data')
                user.first_name = form.first_name.data.upper()
                user.last_name = form.last_name.data.upper()
                user.address = form.address.data
                user.adhar_number = form.adhar_number.data
                user.pan_number = form.pan_number.data.upper()
                user.email = form.email.data.lower()

                db.session.commit()
                flash('update applied', 'success')
                return redirect(url_for('users.update_info'))
    return render_template(
        'update_info.html',
        title='Update User',
        form=form,
        user_form=user_form,
        legend='Update User',
        user_legend='Search User Account')


@users.errorhandler(403)
def not_found_error(error):
    return render_template('403.html')


@users.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html')
