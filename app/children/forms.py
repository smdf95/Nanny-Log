from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, RadioField, SubmitField, SelectField, ValidationError, IntegerField, DateTimeField, DateField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed
from app.models import User
from flask_login import current_user

def validate_not_none(form, field):
    if field.data is None:
        raise ValidationError('Please select a role.')

class ChildForm(FlaskForm):
    """
    Child form
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    picture = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    gender = SelectField('Gender', choices=[(None, 'Select Gender'), ('m', 'Male'), ('f', 'Female'), ('nb', 'Non-Binary'), ('na', 'Prefer not to Say')], default=None, validators=[validate_not_none])
    submit = SubmitField('Submit')
    

class AssignChild(FlaskForm):
    """
    Form for assigning children to parents and nannies
    """
    child = SelectField('Select Child')
    parent = SelectField('Select Parent')
    nanny = SelectField('Select Nanny')
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    """
    For for editing child's profile
    """
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    dob = DateField('Date of Birth')
    picture = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    gender = SelectField('Gender', choices=[(None, 'Select Gender'), ('m', 'Male'), ('f', 'Female'), ('nb', 'Non-Binary'), ('na', 'Prefer not to Say')])
    submit = SubmitField('Make Changes')
