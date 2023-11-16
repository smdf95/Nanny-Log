from datetime import datetime
from flask import render_template, redirect, url_for, flash, Blueprint, request
from app import db
from app.events.forms import ActivitiesForm, SleepForm, FoodForm, DevelopmentalForm, IncidentForm, MedicationForm, NappyForm, NoteForm, CommentForm, PictureForm
from app.events.utils import save_event_picture, get_assigned_children
from app.models import Nanny, Manager, User, Child, Activity, Event, Sleep, Food, Developmental, Incident, Medication, Nappy, Note, Comment, Picture
from flask_login import current_user, login_required

events_blueprint = Blueprint('events', __name__)


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
    form=form, Child=Child)

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
    return render_template('events/developmental.html', title='Developmental', form=form, Child=Child)
        


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
    form=form, Child=Child)

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
    return render_template('events/incident.html', title='Incident', form=form, Child=Child)

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
    return render_template('events/medication.html', title='Medication', form=form, Child=Child)

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
    return render_template('events/nappy.html', title='Nappy', form=form, Child=Child)

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
    return render_template('events/note.html', title='Note', form=form, Child=Child)

@events_blueprint.route('/picture', methods=['GET', 'POST'])
@login_required
def picture():
    form = PictureForm()

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
                    event_type='Picture',
                    user_id=current_id,
                    child_id=kid.child_id,
                )
                db.session.add(event)
                db.session.commit()
                if form.picture.data:
                    picture_file = save_event_picture(form.picture.data)
                    picture = Picture(
                        caption=form.caption.data,
                        picture_file=picture_file,
                        event_id=event.event_id

                    )
                else:
                    picture = Picture(
                        caption=form.caption.data,
                        event_id=event.event_id
                    )

                db.session.add(picture)
                db.session.commit()
            return redirect(url_for('index'))
    return render_template('events/picture.html', title='Picture', form=form, Child=Child)

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
    form=form, Child=Child)


@events_blueprint.route('/post/<int:event_id>', methods=['GET', 'POST'])
@login_required
def post(event_id):
    event = Event.query.get(event_id)
    comments = Comment.query.filter_by(event_id=event_id).order_by(Comment.comment_time.desc()).all()
    

    form = CommentForm()
    if form.validate_on_submit():
        comment_to_add = Comment(
            comment_time=datetime.now(),
            comment_text=form.comment_text.data,
            event_id=event_id,
            user_id=current_user.user_id
        )
        db.session.add(comment_to_add)
        db.session.commit()
        return redirect(url_for('events.post', event_id=event_id))
    return render_template('events/post.html', title='Post', event=event, comments=comments, form=form, User=User)

@events_blueprint.route('/delete_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment.user_id == current_user.user_id:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment successfully deleted!')
    else:
        flash('You can only delete your own comments!')
    return redirect(url_for('events.post', event_id=comment.event_id))



@events_blueprint.route('/delete_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get(event_id)
    comments = Comment.query.filter_by(event_id=event_id).all()
    if comments:
        for comment in comments:
            db.session.delete(comment)
            db.session.commit()
    if event.user_id == current_user.user_id or current_user.role == 'manager':
        db.session.delete(event)
        db.session.commit()
    return redirect(url_for('index'))

