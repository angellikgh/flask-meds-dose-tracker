from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators


class RegisterForm(FlaskForm):
    first_name = StringField("First Name", [validators.InputRequired(message="This field cannot be empty."),
                                            validators.Length(min=2, max=50,
                                                              message="First name must be between 2 to 50 characters.")
                                            ])
    last_name = StringField("Last Name", [validators.InputRequired(message="This field cannot be empty."),
                                          validators.Length(min=2, max=50,
                                                            message="Last name must be between 2 to 50 characters.")])
    email = StringField("Email Address", [validators.InputRequired(message="This field cannot be empty."),
                                          validators.Email(message="That is not a valid email address.")])
    password = PasswordField("Password", [validators.InputRequired(message="This field cannot be empty."),
                                          validators.Length(min=8, message="Password must be at least 8 characters.")])
    submit = SubmitField("Create an account")


class LoginForm(FlaskForm):
    email = StringField("Email Address", [validators.InputRequired(message="This field cannot be empty."),
                                          validators.Email(message="That is not a valid email address.")])
    password = PasswordField("Password", [validators.InputRequired(message="This field cannot be empty."),
                                          validators.Length(min=8, message="Password must be at least 8 characters.")])
    submit = SubmitField("Log in")
