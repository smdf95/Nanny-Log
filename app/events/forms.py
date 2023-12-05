from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    SubmitField, 
    SelectField, 
    ValidationError, 
    SelectMultipleField, 
    widgets, 
    TextAreaField
)
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

def validate_not_none(form, field):
    if field.data is None:
        raise ValidationError('Please select a role.')

class ActivitiesForm(FlaskForm):
    """
    Activities form
    """
    child = SelectMultipleField('Select Children', coerce=int, widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())
    description = TextAreaField('Description', validators=[DataRequired()])
    picture = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')


class DevelopmentalForm(FlaskForm):
    """
    Developmental form
    """
    child = SelectMultipleField('Select Children', coerce=int, widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())
    description = TextAreaField('Description', validators=[DataRequired()])
    picture = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')

class FoodForm(FlaskForm):
    """
    Food form
    """
    child = SelectMultipleField('Select Children', coerce=int, widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())
    meal_type = SelectField('Meal Type', choices=[(None, 'Select Meal Type'), ('bottle', 'Bottle'), ('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner')], default=None, validators=[validate_not_none])
    description = TextAreaField('Description', validators=[DataRequired()])
    picture = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')

class IncidentForm(FlaskForm):
    """
    Incident form
    """
    child = SelectMultipleField('Select Children', coerce=int, widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())
    incident_type = SelectField('Incident Type', choices=[(None, 'Select Incident Type'), ('injury', 'Injury'), ('health', 'Health'), ('behavioural', 'Behavioural'), ('other', 'Other')], default=None, validators=[validate_not_none])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class MedicationForm(FlaskForm):
    """
    Medication form
    """
    child = SelectMultipleField('Select Children', coerce=int, widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())
    medication_name = StringField('Medication Name', validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    reason = TextAreaField('Reason')
    time_given = StringField('Time Given', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NappyForm(FlaskForm):
    """
    Nappy form
    """
    child = SelectMultipleField('Select Children', coerce=int, widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())
    nappy_type = SelectField('Nappy Type', choices=[(None, 'Choose Nappy or Potty'), ('nappy', 'Nappy'), ('potty', 'Potty')], default=None, validators=[validate_not_none])
    condition = TextAreaField('Condition')
    submit = SubmitField('Submit')

class NoteForm(FlaskForm):
    """
    Note form
    """
    child = SelectMultipleField('Select Children', coerce=int, widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PictureForm(FlaskForm):
    """
    Picture form
    """
    child = SelectMultipleField('Select Children', coerce=int, widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())
    caption = StringField('Caption', validators=[DataRequired(), Length(max=100)])
    picture = FileField('Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Submit')

class SleepForm(FlaskForm):
    """
    Sleep form
    """
    child = SelectMultipleField('Select Children', coerce=int, widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())
    sleep_start = StringField('Sleep Start', validators=[DataRequired()])
    sleep_end = StringField('Sleep End', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    """
    Comment form
    """
    comment_text = TextAreaField('Comment Text', validators=[DataRequired(), Length(min=1, max=255)])
    submit = SubmitField('Submit')