from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Required
from wtforms import validators, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired 

class Upload(FlaskForm):
    image = FileField('Profile Picture', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'Images only!'])])
    caption = TextAreaField('Caption', validators=[InputRequired()])

class SignUpForm(FlaskForm):
    firstname = StringField('Firstname', [validators.Required("(Required)")])
    lastname = StringField('Lastname', [validators.Required("(Required)")])
    username = StringField('Username', [validators.Required("(Required)")])
    gender = SelectField('Gender', choices = [('Select','Select Gender'),('Male','Male'),('Female','Female')])
    email = StringField("Email",[validators.Required("(Required)"), validators.Email("(Required)")])
    bio = TextAreaField('Bio', validators=[InputRequired()])
    image = FileField('Profile Picture', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'Images only!'])])
    
    