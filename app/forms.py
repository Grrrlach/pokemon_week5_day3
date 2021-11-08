from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from .models import User

# class flask_wtf.Form()

class PokemonForm(FlaskForm):
    poke_id = StringField('Search for a Pokemon', validators = [DataRequired()])
    # password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enter, Pokemon Trainer. Pokeknowledge awaits!')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators = [DataRequired()])
    last_name = StringField('Last Name', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired(), EqualTo('confirm_password', message="Your passwords didn't match!")])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password', message="Your passwords didn't match!")])
    submit = SubmitField('Register, brave Pokemon Trainer!')
        #NAME OF DEF MUST BE LIKE THIS: validate_email(). FIELD NAME PRECEDED BY "VALIDATE"
    # def validate_email(form, field):
    #     sr = User.query.filter_by(email = field.data).first() #says to give only first result
    def validate_email(form, field): #could be 'self' and field.
        same_email_user = User.query.filter_by(email = field.data).first() #says to give only first result
        #   Like SELECT * FROM user WHERE email = x
        # filter_by will always return a list, even of 1 user
        #.first says to give only 1 user object, instead of a list. 1 row.
        if same_email_user: 
            #will return None if nobody in database. this is for if it doesn't return None
            raise ValidationError ("We already have a Pokemon trainer using that account!")

    # def validate_password(form, field):
    #     if password != confirm_password


    def pw_check (confirm_password):
        if not confirm_password :
            raise ValidationError ("Those passwords do not match!")


