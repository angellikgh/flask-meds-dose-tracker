from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators, IntegerField, SelectField


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
    phone_number = StringField("Phone Number", [validators.InputRequired(message="This field cannot be empty.")])
    password = PasswordField("Password", [validators.InputRequired(message="This field cannot be empty."),
                                          validators.Length(min=8, message="Password must be at least 8 characters.")])
    submit = SubmitField("Create an account")


class LoginForm(FlaskForm):
    email = StringField("Email Address", [validators.InputRequired(message="This field cannot be empty."),
                                          validators.Email(message="That is not a valid email address.")])
    password = PasswordField("Password", [validators.InputRequired(message="This field cannot be empty."),
                                          validators.Length(min=8, message="Password must be at least 8 characters.")])
    submit = SubmitField("Log in")


class MedicineForm(FlaskForm):
    name = StringField("Medicine Name", [validators.InputRequired(message="This field cannot be empty."),
                                         validators.Length(min=2, max=100,
                                                           message="Medicine name must be between 2 to 100 characters.")
                                         ])
    dosage = IntegerField("Dosage", [validators.InputRequired(message="This field cannot be empty.")])
    dosage_unit = SelectField("Dosage Unit", choices=["Drop", "Pill", "Tablet", "Vial", "Others"])
    frequency = SelectField("Frequency", choices=['Daily️', 'Weekly️️', 'Monthly'])
    frequency_unit = SelectField("Frequency Occurrence", choices=['Once', 'Twice', 'Trice', 'Others'])
    submit = SubmitField("Submit")


class CodeForm(FlaskForm):
    code = StringField("Code", [validators.InputRequired(message="This field cannot be empty."),
                                validators.Length(max=6,
                                                  message="The Code must be 6 characters.")
                                ])
    submit = SubmitField("Submit")
