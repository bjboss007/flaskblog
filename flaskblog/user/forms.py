from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators = [DataRequired(), Length(min=2,max=20)])
    email = StringField('email', validators = [DataRequired(), Email()])
    password = PasswordField('password', validators= [DataRequired()])
    confirm_password = PasswordField('confirm Password', 
                                     validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


    def validate_username(self, username):
        user = User.query.filter_by(username= username.data).first()
        if user:
            raise ValidationError('Username taken! Please choose another one')
    
    
    def validate_email(self, email):
        user = User.query.filter_by(email= email.data).first()
        if user:
            raise ValidationError('Email already taken. Please another one')
    
    def validate_password(self, password):
        p_email = self.email.data.split('@')[0]
        if password.data.lower() == p_email.lower():
            raise ValidationError('You cannot use  your email as your password, consider choosing another one')

class LoginForm(FlaskForm):
    email = StringField('email', validators = [DataRequired(), Email()])
    password = PasswordField('password', validators= [DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class UpdateForm(FlaskForm):
    username = StringField('Username', 
                           validators = [DataRequired(), Length(min=2,max=20)])
    email = StringField('email', validators = [DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg','png'])])

    submit = SubmitField('Update')
    
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username= username.data).first()
            if user:
                raise ValidationError('Username taken! Please choose another one')
    
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email= email.data).first()
            if user:
                raise ValidationError('Email already taken. Please choose another one')

class RequestResetForm(FlaskForm):
    email = StringField('email', validators = [DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    
    def validate_email(self, email):
        user = User.query.filter_by(email= email.data).first()
        if user is None:
            raise ValidationError('There is no account with this email. You mush register first.')
    
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('confirm_password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')