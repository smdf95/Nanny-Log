from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed
from app.models import User
from flask_login import current_user

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


class UpdateProfileForm(FlaskForm):
    """
    Update Profile form
    """
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email', validators=[Email()])
    picture = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        """
        Validate email
        """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already in use. Please choose a different email address.')

class RequestResetForm(FlaskForm):
    """
    Request reset password form
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        """
        Validate email
        """
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No account is associated with that email')

class ResetPasswordForm(FlaskForm):
    """
    Reset password form
    """
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class ChangePasswordForm(FlaskForm):
    """
    Change password form
    """
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    new_password2 = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

