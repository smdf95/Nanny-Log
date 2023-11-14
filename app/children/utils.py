import os
import secrets
from datetime import date
from PIL import Image, ExifTags
from functools import wraps
from flask import abort
from app import app
from app.models import Nanny, Parent, Manager, Parent, Child
from flask_login import current_user


from functools import wraps
from flask import abort

def manager_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'manager':
            abort(403)  # Forbidden
        return func(*args, **kwargs)
    return decorated_function


def association_required(func):
    @wraps(func)
    def decorated_function(child_id, *args, **kwargs):
        current_id = current_user.user_id
        child = Child.query.filter_by(child_id=child_id).first()

        if current_user.role == 'manager':
            manager = Manager.query.filter_by(user_id=current_id).first()
            if manager is None or manager.children is None or child not in manager.children:
                abort(403)  # Forbidden
        elif current_user.role == 'nanny':
            nanny = Nanny.query.filter_by(user_id=current_id).first()
            if nanny is None or nanny.children is None or child not in nanny.children:
                abort(403)  # Forbidden
        elif current_user.role == 'parent':
            parent = Parent.query.filter_by(user_id=current_id).first()
            if parent is None or parent.children is None or child not in parent.children:
                abort(403)  # Forbidden
        else:
            # Handle unrecognized role (you may customize this part)
            abort(403)  # Forbidden

        return func(child_id, *args, **kwargs)

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

def get_assigned_parents(user, parent_ids):
    if isinstance(parent_ids, str):
        parent_ids = [parent_ids]  # Transform the single ID into a list

    return Parent.query.filter(Parent.parent_id.in_(parent_ids)).all()

def get_assigned_nannies(user, nanny_ids):
    if isinstance(nanny_ids, str):
        nanny_ids = [nanny_ids]  # Transform the single ID into a list

    return Nanny.query.filter(Nanny.nanny_id.in_(nanny_ids)).all() 



def calculate_age(birth_date):
    today = date.today()
    
    # Calculate the difference in years and months
    age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    age_months = (today.month - birth_date.month) % 12
    
    # Adjust for negative months
    if age_years > 0 and age_months < 0:
        age_years -= 1
        age_months += 12
    
    # Format the age string
    if age_years == 0:
        if age_months == 1:
            return f"{age_months} month old"
        else:
            return f"{age_months} months old"
    elif age_years == 1:
        if age_months == 0:
            return "1 year old"
        elif age_months == 1:
            return "1 year 1 month old"
        else:
            return f"1 year {age_months} months old"
    else:
        if age_months == 0:
            return f"{age_years} years old"
        elif age_months == 1:
            return f"{age_years} years 1 month old"
        else:
            return f"{age_years} years {age_months} months old"

   

