from flask_wtf import FlaskForm
from flask_wtf.file import (
                                FileField,
                                FileAllowed
                            )
from wtforms import (
                        StringField,
                        PasswordField,
                        SubmitField,
                        BooleanField,
                        IntegerField
                    )
from wtforms.validators import (
                                    DataRequired,
                                    Length,
                                    Email,
                                    EqualTo,
                                    ValidationError,
                                    NumberRange
                                )
from bank_management.models import User


class RegistrationForm(FlaskForm):
    first_name = StringField(
                                'first name',
                                validators=[
                                            DataRequired(),
                                            Length(min=2, max=20)
                                            ],
                                render_kw={'placeholder': 'First Name'}
                            )
    last_name = StringField(
                                'last name',
                                validators=[
                                            DataRequired(),
                                            Length(min=2, max=20)
                                            ],
                                render_kw={'placeholder': 'Last Name'}
                            )
    address = StringField(
                            'address',
                            validators=[
                                        DataRequired(),
                                        Length(min=2)
                                        ],
                            render_kw={'placeholder': 'Full address here'}
                        )
    pan_number = StringField(
                                'pan number',
                                validators=[
                                            DataRequired(),
                                            Length(min=10, max=10)
                                            ],
                                render_kw={
                                            'placeholder':
                                            'Put a valid pan Number'}
                            )
    picture = FileField(
                            'Update Profile Picture',
                            validators=[FileAllowed(['jpg', 'png', 'jpeg'])]
                        )
    adhar_number = StringField(
                                'adhar number',
                                validators=[
                                            DataRequired(),
                                            Length(min=12, max=12)
                                            ],
                                render_kw={
                                            'placeholder':
                                            'Put a valid Adhar Number'}
                            )
    email = StringField(
                            'Email',
                            validators=[DataRequired(), Email()],
                            render_kw={
                                        'placeholder':
                                        'Put a valid Email'}
                        )
    password = PasswordField(
                                'Password',
                                validators=[DataRequired()],
                                render_kw={
                                            'placeholder':
                                            'Must be at least ' +
                                            '8 character long ' +
                                            'Conataining At least' +
                                            ' 1 Upper case letter, ' +
                                            '1 lower case letter, ' +
                                            ' 1 special character, ' +
                                            '1 number'}
                            )
    confirm_password = PasswordField(
                                        'Confirm Password',
                                        validators=[
                                                    DataRequired(),
                                                    EqualTo('password')
                                                    ],
                                        render_kw={
                                                    'placeholder':
                                                    'Must match with ' +
                                                    'above password'}
                                    )
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                                    'That email is taken.'
                                    'Please choose a different one.'
                                )

    def validate_pan_number(self, pan_number):
        user = User.query.filter_by(pan_number=pan_number.data).first()
        if(
            user or
                not(
                    pan_number.data.isalnum() and
                    pan_number.data[:5].isalpha() and
                    pan_number.data[5:9].isdigit() and
                    pan_number.data[-1].isalpha()
                    )):
            raise ValidationError('please add correct pan card deatils.')

    def validate_adhar_number(self, adhar_number):
        user = User.query.filter_by(adhar_number=adhar_number.data).first()

        if (
            user and
            adhar_number.data.isdigit() and
                int(adhar_number.data) > 100000000000):
            raise ValidationError('please add correct adhar card deatils.')

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
                                    '1 number and 1 special character.'
                                )


class LoginForm(FlaskForm):
    crn = StringField(
                        'CRN',
                        validators=[DataRequired()]
                    )
    password = PasswordField(
                                'Password',
                                validators=[DataRequired()]
                            )
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AdminLoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    first_name = StringField(
                                'first name',
                                validators=[
                                            DataRequired(),
                                            Length(min=2, max=20)
                                            ]
                            )
    last_name = StringField(
                                'last name',
                                validators=[
                                            DataRequired(),
                                            Length(min=2, max=20)
                                            ]
                            )
    address = StringField(
                            'address',
                            validators=[
                                        DataRequired(),
                                        Length(min=2)
                                        ]
                        )
    pan_number = StringField(
                                'pan number',
                                validators=[
                                            DataRequired(),
                                            Length(min=10, max=10)
                                            ],
                            )
    picture = FileField(
                            'Update Profile Picture(only .jpg, .png or .jpeg)',
                            validators=[FileAllowed(['jpg', 'png', 'jpeg'])],
                        )
    adhar_number = IntegerField(
                                'adhar number',
                                validators=[
                                            DataRequired(),
                                            NumberRange(
                                                        min=100000000000,
                                                        max=999999999999
                                                        )
                                            ]
                            )
    email = StringField(
                            'Email',
                            validators=[DataRequired(), Email()]
                        )
    user_crn = IntegerField(
                                'User CRN',
                                validators=[DataRequired()],
                                render_kw={'readonly': True}
                            )
    submit = SubmitField('Update')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                                    'There is no account with that email.'
                                    ' You must register first.'
                                )


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
                                'Password',
                                validators=[DataRequired()]
                            )
    confirm_password = PasswordField(
                                        'Confirm Password',
                                        validators=[
                                                    DataRequired(),
                                                    EqualTo('password')
                                                    ]
                                    )
    submit = SubmitField('Reset Password')


class SearchUser(FlaskForm):
    user_crn = IntegerField(
                                'Put user crn here',
                                validators=[
                                            DataRequired(),
                                            NumberRange(min=10000, max=99999)
                                            ]
                            )
    user_submit = SubmitField('Search User')


class DeleteUser(FlaskForm):
    account_holder_name = StringField(
                                        'account holder name',
                                        validators=[DataRequired()],
                                        render_kw={'readonly': True}
                                    )
    account_holder_crn = StringField(
                                        'account holder CRN',
                                        validators=[DataRequired()],
                                        render_kw={'readonly': True}
                                    )
    confirm = BooleanField(
                            'Confirm',
                            validators=[DataRequired()]
                        )
    delete_submit = SubmitField('Delete Account')
