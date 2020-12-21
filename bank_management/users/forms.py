from flask_wtf import FlaskForm
from flask_wtf.file import (
    FileField,
    FileAllowed)
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    IntegerField)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    NumberRange)
from bank_management.models import User


class RegistrationForm(FlaskForm):
    first_name = StringField(
        'First Name',
        validators=[
            DataRequired(),
            Length(min=2, max=20)],
        render_kw={'placeholder': 'First Name'})
    last_name = StringField(
        'Last Name',
        validators=[
            DataRequired(),
            Length(min=2, max=20)],
        render_kw={'placeholder': 'Last Name'})
    address = StringField(
        'Address',
        validators=[
            DataRequired(),
            Length(min=2)],
        render_kw={'placeholder': 'Full Address here'})
    pan_number = StringField(
        'Pan Number',
        validators=[
            DataRequired(),
            Length(min=10, max=10)],
        render_kw={
            'placeholder':
            'Put a valid pan Number'
            ' e.g. awerd1256r'})
    picture = FileField(
        'Update Profile Picture',
        validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    adhar_number = StringField(
        'Adhar Number',
        validators=[
            DataRequired(),
            Length(min=12, max=12)],
        render_kw={
            'placeholder':
            'Put a valid Adhar Number '
            'e.g. 123412341234'})
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={
            'placeholder':
            'Put a valid Email'})
    password = PasswordField(
        'Password',
        validators=[DataRequired()],
        render_kw={
            'placeholder':
            'Must be at least '
            '8 character long '
            'Conataining At least'
            ' 1 Upper case letter, '
            '1 lower case letter, '
            ' 1 special character, and '
            '1 number'})
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password')],
        render_kw={
            'placeholder':
            'Must match with '
            'above password'})
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken.'
                'Please choose a different one.')

    def validate_pan_number(self, pan_number):
        user = User.query.filter_by(pan_number=pan_number.data).first()
        if(
            user or not(
                pan_number.data.isalnum()
                and pan_number.data[:5].isalpha() and
                pan_number.data[5:9].isdigit() and
                pan_number.data[-1].isalpha())):
            raise ValidationError('Please add correct pan card deatils.')

    def validate_adhar_number(self, adhar_number):
        user = User.query.filter_by(adhar_number=adhar_number.data).first()

        if user or not(
            adhar_number.data.isdigit() and
                int(adhar_number.data) > 100000000000):
            raise ValidationError('Please add correct adhar card deatils.')

    def validate_first_name(self, first_name):
        if not(first_name.data.isalpha()):
            raise ValidationError('Put valid first name')

    def validate_last_name(self, last_name):
        if not(last_name.data.isalpha()):
            raise ValidationError('Put valid last name')

    def validate_password(self, password):
        if (
                password.data.isalnum() or
                not([char for char in password.data if char.isupper()]) or
                not([char for char in password.data if char.islower()]) or
                not([char for char in password.data if char.isdigit()]) or
                len(password.data) < 8):
            raise ValidationError(
                'Must have at least length of 8 and'
                'also 1 upper case, 1 lower case,'
                '1 number and 1 special character.')


class LoginForm(FlaskForm):
    crn = StringField(
        'CRN',
        validators=[DataRequired()])
    password = PasswordField(
        'Password',
        validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_crn(self, crn):
        if not(crn.data.isdigit()):
            raise ValidationError('Put Right CRN')


class AdminLoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    first_name = StringField(
        'First Name',
        validators=[
            DataRequired(),
            Length(min=2, max=20)])
    last_name = StringField(
        'Last Name',
        validators=[
            DataRequired(),
            Length(min=2, max=20)])
    address = StringField(
        'Address',
        validators=[
            DataRequired(),
            Length(min=2)])
    pan_number = StringField(
        'Pan Number',
        validators=[
            DataRequired(),
            Length(min=10, max=10)])
    picture = FileField(
        'Update Profile Picture(only .jpg, .png or .jpeg)',
        validators=[FileAllowed(['jpg', 'png', 'jpeg'])],)
    adhar_number = StringField(
        'Adhar Number',
        validators=[
            DataRequired(),
            Length(min=12, max=12)])
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()])
    user_crn = IntegerField(
        'User CRN',
        validators=[DataRequired()],
        render_kw={'readonly': True})
    submit = SubmitField('Update')

    def validate_first_name(self, first_name):
        if not(first_name.data.isalpha()):
            raise ValidationError('Put valid first name')

    def validate_last_name(self, last_name):
        if not(last_name.data.isalpha()):
            raise ValidationError('Put valid last name')

    def validate_pan_number(self, pan_number):
        if(not(
                pan_number.data.isalnum()
                and pan_number.data[:5].isalpha() and
                pan_number.data[5:9].isdigit() and
                pan_number.data[-1].isalpha())):
            raise ValidationError('please add correct Pan Card deatils.')

    def validate_adhar_number(self, adhar_number):
        if not(
            adhar_number.data.isdigit() and
                int(adhar_number.data) > 100000000000):
            raise ValidationError('please add correct Adhar Card deatils.')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that email.'
                ' You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password')])
    submit = SubmitField('Reset Password')


class SearchUser(FlaskForm):
    user_crn = IntegerField(
        'Put User CRN here',
        validators=[
            DataRequired(),
            NumberRange(min=10000, max=99999)])
    user_submit = SubmitField('Search User')

    def validate_crn(self, user_crn):
        if not(user_crn.data.isdigit()):
            raise ValidationError('Put Right CRN')


class DeleteUser(FlaskForm):
    account_holder_name = StringField(
        'Account Holder Name',
        validators=[DataRequired()],
        render_kw={'readonly': True})
    account_holder_crn = StringField(
        'Account Holder CRN',
        validators=[DataRequired()],
        render_kw={'readonly': True})
    confirm = BooleanField(
        'Confirm',
        validators=[DataRequired()])
    delete_submit = SubmitField('Delete Account')
