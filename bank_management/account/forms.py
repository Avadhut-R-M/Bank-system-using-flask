from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    SelectField,
    IntegerField,
    BooleanField)
from wtforms.validators import (
    DataRequired,
    NumberRange,
    Length)
from wtforms.fields.html5 import DateField


class AccountForm(FlaskForm):
    account_holder_name = StringField(
        'Account Holder Name',
        render_kw={'readonly': True})
    account_holder_crn = StringField(
        'Account Holder CRN',
        render_kw={'readonly': True})
    account_holder_address = TextAreaField(
        'Account Holder Address',
        render_kw={'readonly': True})
    account_type = SelectField(
        'Choose type of Account',
        choices=[
            ('saving', 'Saving Account'),
            ('current', 'Current Account'),
            ('salary', 'Salary Account')])
    submit = SubmitField('New Account')


class MoneyTranferForm(FlaskForm):
    account_type = SelectField(
        'Choose Type of Account',
        coerce=str)
    receiver_accont_num = IntegerField(
        'Receiver Account Number',
        validators=[
            DataRequired(),
            NumberRange(
                min=100000,
                max=999999)])
    receiver_first_name = StringField(
        'Receiver First Name',
        validators=[
            DataRequired(),
            Length(min=2, max=20)])
    receiver_last_name = StringField(
        'Receiver Last Name',
        validators=[
            DataRequired(),
            Length(min=2, max=20)])
    money_transfer = IntegerField(
        'Amount to be transfered',
        validators=[
            DataRequired(),
            NumberRange(min=1)])
    submit = SubmitField('Confirm Transform')


class SearchUserAccount(FlaskForm):
    account_number = IntegerField(
        'Put Account Number here',
        validators=[
            DataRequired(),
            NumberRange(
                min=100000,
                max=999999)])
    search_submit = SubmitField('Search Account')


class AddRemoveMoney(FlaskForm):
    account_holder_name = StringField(
        'Account Holder Name',
        validators=[DataRequired()],
        render_kw={'readonly': True})
    account_holder_crn = StringField(
        'Account Holder CRN',
        validators=[DataRequired()],
        render_kw={'readonly': True})
    account_type = StringField(
        'Account Type',
        validators=[DataRequired()],
        render_kw={'readonly': True})
    account_number = StringField(
        'account number',
        validators=[DataRequired()],
        render_kw={'readonly': True})
    account_balance = StringField(
        'Account Balance',
        validators=[DataRequired()],
        render_kw={'readonly': True})
    money = IntegerField(
        'Put Amount here',
        validators=[
            DataRequired(),
            NumberRange(min=1)])
    submit = SubmitField('Proceed Transaction')


class DeleteAccount(FlaskForm):
    account_holder_name = StringField(
        'Account Holder Name',
        validators=[DataRequired()],
        render_kw={'readonly': True})
    account_holder_crn = StringField(
        'Account Holder CRN',
        validators=[DataRequired()],
        render_kw={'readonly': True})
    account_type = StringField(
        'Account Type',
        validators=[DataRequired()],
        render_kw={'readonly': True})
    account_number = StringField(
        'Account Number',
        validators=[DataRequired()],
        render_kw={'readonly': True})
    account_balance = StringField(
        'Account Balance',
        validators=[DataRequired()],
        render_kw={'readonly': True})
    confirm = BooleanField('Confirm', validators=[DataRequired()])
    delete_submit = SubmitField('Delete Account')


class AdminLogForm(FlaskForm):
    account_number = IntegerField(
        'Put Account Number Here',
        validators=[
            DataRequired(),
            NumberRange(
                min=100000,
                max=999999)])
    from_date = DateField('From', format='%Y-%m-%d')
    to_date = DateField('To', format='%Y-%m-%d')
    log_submit = SubmitField('Find Log')


class UserLogForm(FlaskForm):
    account_number = SelectField(
        'Choose type of Account',
        coerce=str)
    from_date = DateField('From', format='%Y-%m-%d')
    to_date = DateField('To', format='%Y-%m-%d')
    log_submit = SubmitField('Find Log')
