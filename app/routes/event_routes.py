import os
import secrets
from PIL import Image
from datetime import datetime
from flask import render_template, redirect, url_for, flash, Blueprint, request
from app import app, db
from app.forms import ActivitiesForm, SleepForm, FoodForm, DevelopmentalForm, IncidentForm, MedicationForm, NappyForm, NoteForm
from app.models import Nanny, Manager, Child, Activity, Event, Sleep, Food, Developmental, Incident, Medication, Nappy, Note
from flask_login import current_user, login_required

events_blueprint = Blueprint('events', __name__)

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


@events_blueprint.route('/activities', methods=['GET', 'POST'])
@login_required
def activities():
    form = ActivitiesForm()
    current_id = current_user.user_id
    if current_user.role == 'nanny':
        nanny = Nanny.query.filter_by(user_id=current_id).first()
        form.child.choices = [
            (child.child_id, f"{child.first_name} {child.last_name}") for child in nanny.children
        ]
    elif current_user.role == 'manager':
        manager = Manager.query.filter_by(user_id=current_id).first()
        form.child.choices = [
            (child.child_id, f"{child.first_name} {child.last_name}") for child in manager.children
        ]

    if request.method == 'POST':
        if form.validate_on_submit():
            selected_child_ids = form.child.data
            selected_children = get_assigned_children(current_user, selected_child_ids)
            

            for kid in selected_children:
                event = Event(
                    event_time=datetime.now(),
                    event_type='Activities',
                    user_id=current_id,
                    child_id=kid.child_id,
                )
                db.session.add(event)
                db.session.commit()
                if form.picture.data:
                    picture_file = save_event_picture(form.picture.data)
                    activity = Activity(
                        duration=form.duration.data,
                        description=form.description.data,
                        picture=picture_file,
                        event_id=event.event_id
                    )
                else:
                    activity = Activity(
                        duration=form.duration.data,
                        description=form.description.data,
                        event_id=event.event_id
                    )

                db.session.add(activity)
                db.session.commit()
            return redirect(url_for('index'))
    return render_template('events/activities.html', title='Activities', 
    form=form)

@events_blueprint.route('/developmental', methods=['GET', 'POST'])
@login_required
def developmental():
    form = DevelopmentalForm()

    current_id = current_user.user_id
    if current_user.role == 'nanny':
        nanny = Nanny.query.filter_by(user_id=current_id).first()
        form.child.choices = [
            (child.child_id, f"{child.first_name} {child.last_name}") for child in nanny.children
        ]
    elif current_user.role == 'manager':
        manager = Manager.query.filter_by(user_id=current_id).first()
        form.child.choices = [
            (child.child_id, f"{child.first_name} {child.last_name}") for child in manager.children
        ]


    if request.method == 'POST':
        if form.validate_on_submit():
            selected_child_ids = form.child.data
            selected_children = get_assigned_children(current_user, selected_child_ids)
            

            for kid in selected_children:
                event = Event(
                    event_time=datetime.now(),
                    event_type='Developmental',
                    user_id=current_id,
                    child_id=kid.child_id,
                )
                db.session.add(event)
                db.session.commit()
                if form.picture.data:
                    picture_file = save_event_picture(form.picture.data)
                    developmental = Developmental(
                        description=form.description.data,
                        picture=picture_file,
                        event_id = event.event_id
                    )
                else: 
                    developmental = Developmental(
                        description=form.description.data,
                        event_id = event.event_id

                    )
                db.session.add(developmental)
                db.session.commit()
                flash('Your log has been created!', 'success')
            return redirect(url_for('index'))
    return render_template('events/developmental.html', title='Developmental', form=form)
        


@events_blueprint.route('/food', methods=['GET', 'POST'])
@login_required
def food():
    form = FoodForm()

    current_id = current_user.user_id
    if current_user.role == 'nanny':
        nanny = Nanny.query.filter_by(user_id=current_id).first()
        form.child.choices = [
            (child.child_id, f"{child.first_name} {child.last_name}") for child in nanny.children
        ]
    elif current_user.role == 'manager':
        manager = Manager.query.filter_by(user_id=current_id).first()
        form.child.choices = [
            (child.child_id, f"{child.first_name} {child.last_name}") for child in manager.children
        ]


    if request.method == 'POST':
        if form.validate_on_submit():
            selected_child_ids = form.child.data
            selected_children = get_assigned_children(current_user, selected_child_ids)
            

            for kid in selected_children:
                event = Event(
                    event_time=datetime.now(),
                    event_type='Food',
                    user_id=current_id,
                    child_id=kid.child_id,
                )
                db.session.add(event)
                db.session.commit()

                if form.picture.data:
                    picture_file = save_event_picture(form.picture.data)
                    food = Food(
                        meal_type=form.meal_type.data,
                        description=form.description.data,
                        picture=picture_file,
                        event_id=event.event_id
                    )
                else:
                    food = Food(
                        meal_type=form.meal_type.data,
                        description=form.description.data,
                        event_id=event.event_id
                    )
                    
                db.session.add(food)
                db.session.commit()

            return redirect(url_for('index'))
    return render_template('events/food.html', title='Food', 
    form=form)

@events_blueprint.route('/incident', methods=['GET', 'POST'])
@login_required
def incident():
    form = IncidentForm()

    current_id = current_user.user_id
    if current_user.role == 'nanny':
        nanny = Nanny.query.filter_by(user_id=current_id).first()
        form.child.choices = [
            (child.child_id, f"{child.first_name} {child.last_name}") for child in nanny.children
        ]
    elif current_user.role == 'manager':
        manager = Manager.query.filter_by(user_id=current_id).first()
        form.child.choices = [
            (child.child_id, f"{child.first_name} {child.last_name}") for child in manager.children
        ]


    if request.method == 'POST':
        if form.validate_on_submit():
            selected_child_ids = form.child.data
            selected_children = get_assigned_children(current_user, selected_child_ids)
            

            for kid in selected_children:
                event = Event(
                    event_time=datetime.now(),
                    event_type='Incident',
                    user_id=current_id,
                    child_id=kid.child_id,
                )
                db.session.add(event)
                db.session.commit()
                incident = Incident(
                    incident_type=form.incident_type.data,
                    description=form.description.data,
                    event_id=event.event_id

                )
                db.session.add(incident)
                db.session.commit()
            return redirect(url_for('index'))
    return render_template('events/incident.html', title='Incident', form=form)

@events_blueprint.route('/medication', methods=['GET', 'POST'])
@login_required
def medication():
    form = MedicationForm()

    current_id = current_user.user_id
    if current_user.role == 'nanny':
        nanny = Nanny.query.filter_by(user_id=current_id).first()
        form.child.choices = [
            (child.child_id, f"{child.first_name} {child.last_name}") for child in nanny.children
        ]
    elif current_user.role == 'manager':
        manager = Manager.query.filter_by(user_id=current_id).first()
        form.child.choices = [
            (child.child_id, f"{child.first_name} {child.last_name}") for child in manager.children
        ]


    if request.method == 'POST':
        if form.validate_on_submit():
            selected_child_ids = form.child.data
            selected_children = get_assigned_children(current_user, selected_child_ids)
            

            for kid in selected_children:
                event = Event(
                    event_time=datetime.now(),
                    event_type='Medication',
                    user_id=current_id,
                    child_id=kid.child_id,
                )
                db.session.add(event)
                db.session.commit()
                medication = Medication(
                    medication_name=form.medication_name.data,
                    amount=form.amount.data,
                    reason=form.reason.data,
                    time_given=form.time_given.data,
                    event_id=event.event_id

                )
                db.session.add(medication)
                db.session.commit()
            return redirect(url_for('index'))
    return render_template('events/medication.html', title='Medication', form=form)

@events_blueprint.route('/nappy', methods=['GET', 'POST'])
@login_required
def nappy():
    form = NappyForm()

    current_id = current_user.user_id
    if current_user.role == 'nanny':
        nanny = Nanny.query.filter_by(user_id=current_id).first()
        form.child.choices = [
            (child.child_id, f"{child.first_name} {child.last_name}") for child in nanny.children
        ]
    elif current_user.role == 'manager':
        manager = Manager.query.filter_by(user_id=current_id).first()
        form.child.choices = [
            (child.child_id, f"{child.first_name} {child.last_name}") for child in manager.children
        ]


    if request.method == 'POST':
        if form.validate_on_submit():
            selected_child_ids = form.child.data
            selected_children = get_assigned_children(current_user, selected_child_ids)
            

            for kid in selected_children:
                event = Event(
                    event_time=datetime.now(),
                    event_type='Nappy',
                    user_id=current_id,
                    child_id=kid.child_id,
                )
                db.session.add(event)
                db.session.commit()
                nappy = Nappy(
                    nappy_type=form.nappy_type.data,
                    condition=form.condition.data,
                    event_id=event.event_id

                )
                db.session.add(nappy)
                db.session.commit()
            return redirect(url_for('index'))
    return render_template('events/nappy.html', title='Nappy', form=form)

@events_blueprint.route('/note', methods=['GET', 'POST'])
@login_required
def note():
    form = NoteForm()

    current_id = current_user.user_id
    if current_user.role == 'nanny':
        nanny = Nanny.query.filter_by(user_id=current_id).first()
        form.child.choices = [
            (child.child_id, f"{child.first_name} {child.last_name}") for child in nanny.children
        ]
    elif current_user.role == 'manager':
        manager = Manager.query.filter_by(user_id=current_id).first()
        form.child.choices = [
            (child.child_id, f"{child.first_name} {child.last_name}") for child in manager.children
        ]


    if request.method == 'POST':
        if form.validate_on_submit():
            selected_child_ids = form.child.data
            selected_children = get_assigned_children(current_user, selected_child_ids)
            

            for kid in selected_children:
                event = Event(
                    event_time=datetime.now(),
                    event_type='Note',
                    user_id=current_id,
                    child_id=kid.child_id,
                )
                db.session.add(event)
                db.session.commit()
                note = Note(
                    description=form.description.data,
                    event_id=event.event_id

                )
                db.session.add(note)
                db.session.commit()
            return redirect(url_for('index'))
    return render_template('events/note.html', title='Note', form=form)

@events_blueprint.route('/sleep', methods=['GET', 'POST'])
@login_required
def sleep():
    form = SleepForm()

    current_id = current_user.user_id
    if current_user.role == 'nanny':
        nanny = Nanny.query.filter_by(user_id=current_id).first()
        form.child.choices = [
            (child.child_id, f"{child.first_name} {child.last_name}") for child in nanny.children
        ]
    elif current_user.role == 'manager':
        manager = Manager.query.filter_by(user_id=current_id).first()
        form.child.choices = [
            (child.child_id, f"{child.first_name} {child.last_name}") for child in manager.children
        ]


    if request.method == 'POST':
        if form.validate_on_submit():
            selected_child_ids = form.child.data
            selected_children = get_assigned_children(current_user, selected_child_ids)
            

            for kid in selected_children:
                event = Event(
                    event_time=datetime.now(),
                    event_type='Sleep',
                    user_id=current_id,
                    child_id=kid.child_id,
                )
                db.session.add(event)
                db.session.commit()
                sleep = Sleep(
                    sleep_start=form.sleep_start.data,
                    sleep_end=form.sleep_end.data,
                    event_id=event.event_id
                )
                db.session.add(sleep)
                db.session.commit()
            return redirect(url_for('index'))
    return render_template('events/sleep.html', title='Sleep', 
    form=form)