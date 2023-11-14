import os
import secrets
from PIL import Image
from functools import wraps
from flask import abort
from app import app
from app.models import Child
from flask_login import current_user

def save_event_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/event_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn

def get_assigned_children(user, child_ids):
    if not isinstance(child_ids, list):
        child_ids = [child_ids]  # Transform the single ID into a list

    return Child.query.filter(Child.child_id.in_(child_ids)).all()