from flask import (
    render_template,
    url_for,
    flash,
    redirect,
    abort,
    Blueprint)
from flask_login import (
    current_user,
    login_required)
from bank_management import db
from bank_management.models import (
    Account,
    Log,
    User)
from bank_management.account.forms import (
    AccountForm,
    MoneyTranferForm,
    SearchUserAccount,
    AddRemoveMoney,
    DeleteAccount,
    AdminLogForm,
    UserLogForm)
from random import randint

account = Blueprint('accounts', __name__)


@account.route("/account/create", methods=['GET', 'POST'])
@login_required
def create_account():
    form = AccountForm()
    form.account_holder_name.data = (
        current_user.first_name + '  '
        + current_user.last_name)
    form.account_holder_crn.data = current_user.crn
    form.account_holder_address.data = current_user.address
    if form.validate_on_submit():

        while(1):
            account_number = randint(100000, 999999)
            account_user = Account.query\
                .filter_by(account_no=account_number).first()
            if not(account_user):
                break

        if Account.query.filter_by(
            user_id=current_user.crn,
            account_type=form.account_type.data)\
                .first():
            flash(
                'Cannot create same type of account more than once',
                'danger')

        else:
            account = Account(
                user_id=current_user.crn,
                account_type=form.account_type.data,
                account_no=account_number
            )

            db.session.add(account)
            db.session.commit()

            log = Log(
                account_log=(
                    'Created a ' +
                    form.account_type.data +
                    ' account'),
                user_crn=current_user.crn,
                balance=0,
                account_id=account_number)

            db.session.add(log)
            db.session.commit()

            flash('Your account has been created!', 'success')
            return redirect(url_for('main.home'))

    return render_template(
        'create_account.html',
        title='New Account',
        form=form,
        legend='New Account')


@account.route("/account/balance", methods=['GET', 'POST'])
@login_required
def balance():
    if current_user.is_admin:
        abort(403)
    user = current_user
    accounts = Account.query.filter_by(user_id=user.crn)\
        .order_by(Account.account_type.desc()).all()
    return render_template('balance_check.html', accounts=accounts, user=user)


@account.route("/account/money/transfer", methods=['GET', 'POST'])
@login_required
def money_transfer():
    if current_user.is_admin:
        abort(403)
    form = MoneyTranferForm()
    user = current_user
    accounts = Account.query.filter_by(user_id=user.crn).all()
    form.account_type.choices = [
        (u.account_no, u.account_type.capitalize())
        for u in accounts]
    if form.validate_on_submit():
        main_user_account = Account\
            .query\
            .filter_by(
                user_id=user.crn,
                account_no=form.account_type.data)\
            .first()
        other_user_account = Account\
            .query\
            .filter_by(account_no=form.receiver_accont_num.data).first()

        out = True
        if (
                form.receiver_first_name.data.isalpha() and
                form.receiver_last_name.data.isalpha()):
            user_ac = Account\
                .query\
                .filter_by(account_no=form.receiver_accont_num.data)\
                .first()

            if user_ac:
                user = User.query.filter_by(crn=user_ac.user_id).first()
                first_name = form.receiver_first_name.data
                last_name = form.receiver_last_name.data
                if (
                        user and
                        user.first_name == first_name.upper() and
                        user.last_name == last_name.upper()):
                    out = False
        if out:
            flash('Plese check details of reciver', 'danger')

        elif main_user_account.account_no == other_user_account.account_no:
            flash('You cant send money to same account', 'danger')

        else:
            money = form.money_transfer.data
            if money > main_user_account.balance:
                flash('You dose not have enough money to transfer.', 'danger')
                return render_template(
                    'money_transfer.html',
                    title='Money Transfer',
                    form=form,
                    legend='Money Transfer')
            main_user_account.balance -= money
            other_user_account.balance += money
            db.session.commit()
            log1 = Log(
                account_log='Rs. ' + str(money) + ' debited for ' +
                            str(user.first_name),
                debit=money,
                user_crn=main_user_account.user_id,
                balance=main_user_account.balance,
                account_id=main_user_account.account_no)
            db.session.add(log1)
            log2 = Log(
                account_log='Rs. ' + str(money) + ' credited from ' +
                            str(current_user.first_name),
                credit=money,
                user_crn=other_user_account.user_id,
                balance=other_user_account.balance,
                account_id=other_user_account.account_no)
            db.session.add(log2)
            db.session.commit()
            flash('money has been transfered', 'success')
            return redirect(url_for('main.home'))

    return render_template(
        'money_transfer.html',
        title='Money Transfer',
        form=form,
        legend='Money Transfer')


@account.route("/account/money/add", methods=['GET', 'POST'])
@login_required
def money_add():
    if current_user.is_admin is False:
        abort(403)
    account_form = SearchUserAccount()
    form = AddRemoveMoney()
    if account_form.search_submit.data and account_form.validate_on_submit():
        user_account_number = account_form.account_number.data
        user_account = Account.query\
            .filter_by(account_no=user_account_number).first()

        if user_account:
            user = User.query.filter_by(crn=user_account.user_id).first()
            form.account_holder_name.data = (
                user.first_name +
                '  '
                + user.last_name)
            form.account_holder_crn.data = user.crn
            form.account_type.data = user_account.account_type
            form.account_number.data = user_account.account_no
            form.account_balance.data = user_account.balance
            return render_template(
                'addremovemoney.html',
                title='Add Money',
                form=form,
                account_form=account_form,
                legend='Add Money',
                user_legend='Search User')
        else:
            flash('Check user details', 'danger')
    if form.submit.data and form.validate_on_submit():
        user_account_number = account_form.account_number.data
        user_account = Account\
            .query.filter_by(account_no=user_account_number).first()
        if user_account:
            user = User.query.filter_by(crn=user_account.user_id).first()
            user_account.balance += form.money.data
            db.session.commit()
            log = Log(
                account_log=f'Rs. {form.money.data} credited',
                credit=form.money.data,
                user_crn=user_account.user_id,
                balance=user_account.balance,
                account_id=user_account.account_no)
            db.session.add(log)
            db.session.commit()
            flash('Amount added to account', 'success')
            return redirect(url_for('accounts.money_add'))
    return render_template(
        'addremovemoney.html',
        title='Add Money',
        form=form,
        account_form=account_form,
        legend='Add Money',
        user_legend='Search User')


@account.route("/account/money/remove", methods=['GET', 'POST'])
@login_required
def money_remove():
    if current_user.is_admin is False:
        abort(403)
    account_form = SearchUserAccount()
    form = AddRemoveMoney()
    if account_form.search_submit.data and account_form.validate_on_submit():
        user_account_number = account_form.account_number.data
        user_account = Account\
            .query.filter_by(account_no=user_account_number).first()

        if user_account:
            user = User.query.filter_by(crn=user_account.user_id).first()
            form.account_holder_name.data = (
                user.first_name +
                '  '
                + user.last_name)
            form.account_holder_crn.data = user.crn
            form.account_type.data = user_account.account_type
            form.account_number.data = user_account.account_no
            form.account_balance.data = user_account.balance
            return render_template(
                'addremovemoney.html',
                title='Remove Money',
                form=form,
                account_form=account_form,
                legend='Remove Money',
                user_legend='Search User')
        else:
            flash('Check user details', 'danger')

    if form.submit.data and form.validate_on_submit():
        user_account_number = account_form.account_number.data
        user_account = Account\
            .query.filter_by(account_no=user_account_number).first()
        if user_account:
            user = User.query.filter_by(crn=user_account.user_id).first()
            if user_account.balance > form.money.data:
                user_account.balance -= form.money.data
                db.session.commit()
                log = Log(
                    account_log=f'Rs. {form.money.data} debited',
                    debit=form.money.data,
                    user_crn=user_account.user_id,
                    balance=user_account.balance,
                    account_id=user_account.account_no)
                db.session.add(log)
                db.session.commit()
                flash('money successfully debited', 'success')
                return redirect(url_for('accounts.money_remove'))
            else:
                flash('Money is not sufficient for transaction', 'danger')
    return render_template(
        'addremovemoney.html',
        title='Remove Money',
        form=form,
        account_form=account_form,
        legend='Remove Money',
        user_legend='Search User')


@account.route("/account/delete/account", methods=['GET', 'POST'])
@login_required
def remove_account():
    if current_user.is_admin is False:
        abort(403)
    account_form = SearchUserAccount()
    form = DeleteAccount()
    if account_form.search_submit.data and account_form.validate_on_submit():
        user_account_number = account_form.account_number.data
        user_account = Account\
            .query.filter_by(account_no=user_account_number).first()
        if user_account:
            user = User.query.filter_by(crn=user_account.user_id).first()
            if user:
                form.account_holder_name.data = (
                    user.first_name +
                    '  ' +
                    user.last_name)
                form.account_holder_crn.data = user.crn
                form.account_type.data = user_account.account_type.capitalize()
                form.account_number.data = user_account.account_no
                form.account_balance.data = user_account.balance
        else:
            flash('Check User Deatils', 'danger')

    if form.delete_submit.data and form.validate_on_submit():
        user_account_number = account_form.account_number.data
        user_account = Account\
            .query.filter_by(account_no=user_account_number).first()
        if user_account:
            db.session.delete(user_account)
            db.session.commit()
            flash('Account successfully removed', 'success')
            return redirect(url_for('accounts.remove_account'))
    return render_template(
        'delete_account.html',
        title='Delete Account',
        form=form,
        account_form=account_form,
        legend='Delete Account',
        user_legend='Search User Account')


@account.route("/admin/account/log", methods=['GET', 'POST'])
@login_required
def find_log():
    if current_user.is_admin is False:
        abort(403)
    form = AdminLogForm()
    if form.validate_on_submit():
        logs = Log.query.filter_by(account_id=form.account_number.data)\
            .filter(form.from_date.data < Log.account_log_date)\
            .filter(Log.account_log_date <= form.to_date.data)\
            .order_by(Log.account_log_date.desc()).all()

        return render_template('log_show.html', logs=logs)

    return render_template(
        'logs_main.html',
        form=form,
        legend='log',
        titile='log')


@account.route("/account/log", methods=['GET', 'POST'])
@login_required
def account_log():
    if current_user.is_admin:
        abort(403)
    form = UserLogForm()
    user = current_user
    accounts = Account.query.filter_by(user_id=user.crn).all()
    form.account_number.choices = [
        (u.account_no, u.account_type)
        for u in accounts]
    if form.validate_on_submit():
        logs = Log.query.filter_by(account_id=form.account_number.data)\
            .filter(form.from_date.data < Log.account_log_date)\
            .filter(Log.account_log_date <= form.to_date.data)\
            .order_by(Log.account_log_date.desc()).all()

        return render_template('log_show.html', logs=logs)

    return render_template(
        'logs_main.html',
        form=form,
        legend='log',
        titile='log')


@account.errorhandler(403)
def not_found_error(error):
    return render_template('403.html')


@account.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html')
