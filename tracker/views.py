from tracker import app, db, login_manager
from tracker.forms import RegisterForm, LoginForm
from tracker.models import Users
from flask import render_template, flash, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


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
            return redirect(url_for('profile'))
    return render_template('auth/login.html', form=form)
