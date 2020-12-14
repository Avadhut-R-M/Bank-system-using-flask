
import os
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from bank_management import mail


def save_picture(form_picture, crn):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(crn) + f_ext
    picture_path = os.path.join(
                                    current_app.root_path,
                                    'static/profile_pics',
                                    picture_fn
                                )

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
        {url_for('users.reset_token', token=token, _external=True)}

        If you did not make this request then'
        simply ignore this email and no changes will be made.
        '''
    mail.send(msg)


def send_new_user_email(user):
    msg = Message('New account',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''You have been created a new account your credientials are
        CRN = {user.crn}
        Name = {user.first_name} {user.last_name}
        login using password.
        visit the following link:
        {url_for('main.home')}
        '''
    mail.send(msg)
