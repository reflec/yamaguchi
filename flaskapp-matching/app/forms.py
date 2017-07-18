from flask_wtf import FlaskForm as Form
from wtforms import StringField,BooleanField, TextAreaField
from wtforms.validators import Required, Length

#flask web development
from wtforms import SubmitField,PasswordField,ValidationError
from .models import User,Day
from wtforms.validators import Email,Regexp,EqualTo



class LoginForm(Form):
    email = StringField('Email', validators = [Required(),
    Length(1,64),Email()])
    password = PasswordField('Passwrod',validators=[Required()])
    remember_me = BooleanField('Keep me logged in', default = False)
    submit = SubmitField('Log In')


class EditForm(Form):
    nickname = StringField('nickname', validators=[Required()])
    gender = StringField('gender')
    about_me = TextAreaField('about_me',validators=[Length(min=0,max=140)])
    def __init__(self,original_nickname,*args,**kwargs):
        Form.__init__(self,*args,**kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user != None:
            self.nickname.errors.append('This nickname is already is use. Please choose an other one,')
            return False
        return True
        

class DayForm(Form):
    possible_day =  StringField('possible_day', validators=[Required()])

        
    
class SearchForm(Form):
    search = StringField('search',validators=[Required()])

class CalendarForm(Form):
    calendar_data = StringField('calendar_data',validators=[Required()])


class RegistrationForm(Form):
    email = StringField('Email',validators=[Required(),Length(1,64),
    Email()])
    nickname = StringField('nickname',validators=[Required(),Length(1,64),
    Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Nickname must have only letters,'
    'numbers,dots or underscores')])
    password = PasswordField('password',validators=[
    Required(),EqualTo('password2',message='Passwords must match.')])
    password2 = PasswordField('Confirm password',validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_nickname(self,field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('Nickname already in use.')
