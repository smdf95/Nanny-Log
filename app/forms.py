from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, RadioField, SubmitField, SelectField, ValidationError, IntegerField, DateTimeField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed

def validate_not_none(form, field):
    if field.data is None:
        raise ValidationError('Please select a role.')


class LoginForm(FlaskForm):
    """
    Login form
    """
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    """
    Registration form
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    role = SelectField('Role', choices=[(None, 'Select Role'),('manager', 'Manager'), ('nanny', 'Nanny'), ('parent', 'Parent')], default=None, validators=[validate_not_none])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

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

class ActivitiesForm(FlaskForm):
    """
    Activities form
    """
    child = SelectField('Select Child')
    duration = IntegerField('Duration in Minutes', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    picture = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')


class DevelopmentalForm(FlaskForm):
    """
    Developmental form
    """
    child = SelectField('Select Child')
    description = StringField('Description', validators=[DataRequired()])
    picture = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')

class FoodForm(FlaskForm):
    """
    Food form
    """
    child = SelectField('Select Child')
    meal_type = SelectField('Meal Type', choices=[(None, 'Select Meal Type'), ('bottle', 'Bottle'), ('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner')], default=None, validators=[validate_not_none])
    description = StringField('Description', validators=[DataRequired()])
    picture = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')

class IncidentForm(FlaskForm):
    """
    Incident form
    """
    child = SelectField('Select Child')
    incident_type = SelectField('Incident Type', choices=[(None, 'Select Incident Type'), ('injury', 'Injury'), ('health', 'Health'), ('behavioural', 'Behavioural'), ('other', 'Other')], default=None, validators=[validate_not_none])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class MedicationForm(FlaskForm):
    """
    Medication form
    """
    child = SelectField('Select Child')
    medication_name = StringField('Medication Name', validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    reason = StringField('Reason')
    time_given = StringField('Time Given', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NappyForm(FlaskForm):
    """
    Nappy form
    """
    child = SelectField('Select Child')
    nappy_type = SelectField('Nappy Type', choices=[(None, 'Choose Nappy or Potty'), ('nappy', 'Nappy'), ('potty', 'Potty')], default=None, validators=[validate_not_none])
    condition = StringField('Condition')
    submit = SubmitField('Submit')

class NoteForm(FlaskForm):
    """
    Note form
    """
    child = SelectField('Select Child')
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SleepForm(FlaskForm):
    """
    Sleep form
    """
    child = SelectField('Select Child')
    sleep_start = StringField('Sleep Start', validators=[DataRequired()])
    sleep_end = StringField('Sleep End', validators=[DataRequired()])
    submit = SubmitField('Submit')