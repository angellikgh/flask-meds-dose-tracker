from tracker import app, login_manager
from tracker.forms import *
from tracker.models import *
from flask import render_template, flash, url_for, redirect, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from phonenumbers import NumberParseException, is_possible_number, parse, is_valid_number
import os
from dotenv import load_dotenv
load_dotenv()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


# Twilio configs
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
service_sid = os.environ.get('SERVICE_SID')
client = Client(account_sid, auth_token)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile/<name>', methods=['GET', 'POST'])
@login_required
def profile(name):
    medicines = Medicines.query.filter_by(user_id=current_user.id)
    form = MedicineForm()
    if form.validate_on_submit():
        name = form.name.data.title()
        dosage = form.dosage.data
        dosage_unit = form.dosage_unit.data
        frequency = form.frequency.data
        frequency_unit = form.frequency_unit.data

        # Make medication does not exist
        if Medicines.query.filter_by(name=name).first():
            flash("That medication info already exist in the database", "danger")
            return redirect(request.referrer)
        else:
            new_meds = Medicines(
                name=name,
                dosage=dosage,
                dosage_unit=dosage_unit,
                frequency=frequency,
                frequency_unit=frequency_unit,
                user_id=current_user.id
            )
            db.session.add(new_meds)
            db.session.commit()
            flash(f'"{name}" medication info added successfully', "success")
            return redirect(request.referrer)
    return render_template('profile.html', form=form, medicines=medicines)


@app.route('/edit/<int:med_id>', methods=['GET', 'POST'])
@login_required
def edit(med_id):
    medicine = Medicines.query.get(med_id)
    edit_medication = MedicineForm(
        name=medicine.name,
        dosage=medicine.dosage,
        dosage_unit=medicine.dosage_unit,
        frequency=medicine.frequency,
        frequency_unit=medicine.frequency_unit
    )
    if edit_medication.validate_on_submit():
        medicine.name = edit_medication.name.data.title()
        medicine.dosage = edit_medication.dosage.data
        medicine.dosage_unit = edit_medication.dosage_unit.data
        medicine.frequency = edit_medication.frequency.data
        medicine.frequency_unit = edit_medication.frequency_unit.data
        db.session.commit()
        flash(f'"{medicine.name}" medication updated successfully', "success")
        return redirect(url_for('profile', name=current_user.first_name))
    return render_template('edit_medication.html', form=edit_medication)


@app.route("/delete/<int:med_id>")
def delete(med_id):
    delete_med = Medicines.query.get(med_id)
    db.session.delete(delete_med)
    db.session.commit()
    flash("Medication deleted successfully", "success")
    return redirect(request.referrer)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        flash("You are unable to view that page because you are currently logged in.", "info")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        first_name = form.first_name.data.title()
        last_name = form.last_name.data.title()
        email = form.email.data
        phone_number = form.phone_number.data
        password = form.password.data

        try:
            number = parse(phone_number)
            if not is_possible_number(number):
                flash("Check the phone number again", "danger")
                return redirect(request.referrer)
            elif not is_valid_number(number):
                flash("Invalid phone number", "danger")
                return redirect(request.referrer)
        except NumberParseException:
            flash("Add the country code to phone number, eg. +353", "danger")
            return redirect(request.referrer)
        else:
            # Make sure the email does not exist
            if Users.query.filter_by(email=email).first():
                flash("That email exists in the database, try another", "danger")
            elif Users.query.filter_by(phone_number=phone_number).first():
                flash("That number exists in the database, try another", "danger")
            else:
                encrypt_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

                new_user = Users(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    password=encrypt_password,
                )
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)

                verify = client.verify.services(service_sid)
                try:
                    verify.verifications.create(to=current_user.phone_number, channel='sms')
                except TwilioException:
                    verify.verifications.create(to=current_user.phone_number, channel='call')
                flash(f'Registration successful {first_name}, Verify your phone number', "success")
                return redirect(url_for('verify_code'))
    return render_template('auth/register.html', form=form)


@app.route('/verify_code', methods=['GET', 'POST'])
@login_required
def verify_code():
    form = CodeForm()
    if current_user.verified:
        flash("You are already verified.", "info")
        return redirect(url_for('profile', name=current_user.first_name))
    else:
        if form.validate_on_submit():
            code = form.code.data
            user = Users.query.filter_by(first_name=current_user.first_name).first()
            verify = client.verify.services(service_sid)
            check = verify.verification_checks.create(to=current_user.phone_number, code=code)

            if check.status == 'expired':
                try:
                    verify.verifications.create(to=user.phone_number, channel='sms')
                except TwilioException:
                    verify.verifications.create(to=user.phone_number, channel='call')
                else:
                    flash("That code has expired but another has been sent.", "warning")
                    return redirect(request.referrer)

            if check.status == 'approved':
                user.verified = True
                db.session.commit()
                flash("You are verified, you can now set a reminder alert.", "success")
                return redirect(url_for('profile', name=current_user.first_name))
            else:
                flash("Wrong Code", "danger")
                return redirect(request.referrer)
    return render_template('auth/verify_code.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        flash("You are unable to view that page because you are currently logged in.", "info")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Find the user by email
        user = Users.query.filter_by(email=email).first()

        if not user:
            flash("Invalid email address, try again.", "danger")
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, try again.', "danger")
        else:
            login_user(user)
            flash('You are logged in successfully', "success")
            return redirect(url_for('profile', name=current_user.first_name))
    return render_template('auth/login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You are logged out successfully', "success")
    return redirect(url_for('login'))
