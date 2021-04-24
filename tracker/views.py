from tracker import app
from flask import render_template
from tracker.forms import RegisterForm


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        pass
    return render_template('auth/register.html', form=form)

