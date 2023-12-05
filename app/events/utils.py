import os
import secrets
from PIL import Image, ExifTags
from app import app
from app.models import Child
from flask_login import current_user

def save_event_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/event_pics', picture_fn)

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

def get_assigned_children(child_ids):
    if not isinstance(child_ids, list):
        child_ids = [child_ids] 

    return Child.query.filter(Child.child_id.in_(child_ids)).all()
