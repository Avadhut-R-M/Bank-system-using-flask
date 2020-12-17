from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from bank_management import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True)
    crn = db.Column(
        db.Integer,
        unique=True,
        nullable=False)
    first_name = db.Column(
        db.String(20),
        nullable=False)
    last_name = db.Column(
        db.String(20),
        nullable=False)
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False)
    address = db.Column(db.Text(), nullable=False)
    image_file = db.Column(
        db.String(50),
        nullable=False,
        default='default.jpg')
    pan_number = db.Column(db.String(10))
    adhar_number = db.Column(db.String(12))
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    account_holder = db.relationship(
        'Account',
        backref='account_holder',
        passive_deletes=True, lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}'"


class Account(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True)
    account_no = db.Column(
        db.Integer,
        unique=True,
        nullable=False,
        default=0)
    account_type = db.Column(
        db.String(30),
        nullable=False)
    balance = db.Column(
        db.Float,
        nullable=False,
        default=0)
    date_started = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.crn', ondelete='CASCADE'),
        nullable=False)
    account = db.relationship(
        'Log',
        backref='account',
        passive_deletes=True,
        lazy=True)

    def __repr__(self):
        return f"Account('{self.account_no}', '{self.account_type}')"


class Log(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True)
    account_log_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow)
    account_log = db.Column(
        db.String(30),
        nullable=False)
    debit = db.Column(db.Integer)
    credit = db.Column(db.Integer)
    user_crn = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    account_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'account.account_no',
            ondelete='CASCADE'),
        nullable=False)
