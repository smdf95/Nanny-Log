from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    SubmitField, 
    SelectField, 
    ValidationError, 
    DateField, 
    SelectMultipleField, 
    widgets
)
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


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
    child = SelectMultipleField('Select Children', coerce=int, widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())
    parent = SelectMultipleField('Select Parent', coerce=int, widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())
    nanny = SelectMultipleField('Select Nanny', coerce=int, widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())
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
