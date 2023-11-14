import os
import secrets
from PIL import Image, ExifTags
from functools import wraps
from flask import url_for, abort
from app import app, mail
from app.models import Child
from flask_login import current_user
from flask_mail import Message


from functools import wraps
from flask import abort

def manager_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'manager':
            abort(403)  # Forbidden
        return func(*args, **kwargs)
    return decorated_function


def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    i = Image.open(form_picture)
    
    # Check for orientation information in Exif data
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif_data = dict(i._getexif().items())
        if orientation in exif_data:
            if exif_data[orientation] == 3:
                i = i.transpose(Image.ROTATE_180)
            elif exif_data[orientation] == 6:
                i = i.transpose(Image.ROTATE_270)
            elif exif_data[orientation] == 8:
                i = i.transpose(Image.ROTATE_90)
    except (AttributeError, KeyError, IndexError):
        # In case of missing Exif data
        pass

    output_size = (250, 250)
    i.thumbnail(output_size)

    i.save(picture_path, quality=95)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To initiate the password reset process, please click on the link below:
{url_for('main.reset_password', token=token, _external=True)}
If you haven't requested this password reset, you can disregard this email, and no changes will be made to your account.'''

    mail.send(msg)