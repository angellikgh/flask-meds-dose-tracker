from tracker import app, db, login_manager
from tracker.forms import RegisterForm, LoginForm, MedicineForm
from tracker.models import Users, Medicines
from flask import render_template, flash, url_for, redirect, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile/<name>', methods=['GET', 'POST'])
@login_required
def profile(name):
    user = Users.query.filter_by(first_name=name).first_or_404()
    medicines = Medicines.query.all()
    med_count = 0
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
                frequency_unit=frequency_unit
            )
            db.session.add(new_meds)
            db.session.commit()
            flash(f'"{name}" medication info added successfully', "success")
            return redirect(request.referrer)
    return render_template('profile.html', profile=user, form=form, medicines=medicines, med_count=med_count)


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
        password = form.password.data

        # Make sure the email does not exist
        if Users.query.filter_by(email=email).first():
            flash("That email exists in the database, try another", "danger")
        else:
            encrypt_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

            new_user = Users(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=encrypt_password,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)

            flash(f'Registration successful {first_name}, Start tracking...', "success")
            return redirect(url_for('profile'))
    return render_template('auth/register.html', form=form)


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
