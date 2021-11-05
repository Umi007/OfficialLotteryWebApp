import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, ValidationError, Length, EqualTo


# creating excluded character validator
def character_check(form, field):
    excluded_chars = "* ? ! ' ^ + % & / ( ) = } ] [ { $ # @ < >"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f"Character {char} is not allowed.")


# creating phone validator
def phone_check(form, field):
    validate = 1
    if field.data[4] != "-" and field.data[8] != "-":
        validate = 0
    field.data = field.data.replace("-", "")
    for i in field.data:
        if i.isdigit() == False and len(field.data) != 10:
            validate = 0
    if validate == 0:
        raise ValidationError("Phone must be of the form XXXX-XXX-XXXX, including the dashes!")


# setting up the register form
class RegisterForm(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    firstname = StringField(validators=[Required(), character_check])
    lastname = StringField(validators=[Required(), character_check])
    phone = StringField(validators=[Required(), phone_check])
    password = PasswordField(validators=[Required(), Length(min=6, max=12, message='Password must be between 6 and 12 '
                                                                                   'characters in length.')])
    confirm_password = PasswordField(validators=[Required(), EqualTo('password', message='Both password fields must '
                                                                                         'be equal!')])
    pin_key = StringField(validators=[Required(), Length(min=32, max=32, message='PIN key must be 32 characters '
                                                                                 'in length.')])
    submit = SubmitField()

    # creating validating password function
    def validate_password(self, password):
        p = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!\"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~])')
        if not p.match(self.password.data):
            raise ValidationError(
                "Password must contain at least 1 digit, 1 uppercase letter, 1 lowercase letter and 1 special "
                "character.")


# setting up the log in form
class LoginForm(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    password = PasswordField(validators=[Required()])
    pin = StringField(validators=[Required(), Length(min=6, max=6, message='Pin must be 6 digits')])
    submit = SubmitField()
