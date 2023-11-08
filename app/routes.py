import os
import secrets
from PIL import Image
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash
from app import app, db, bcrypt, login_manager
from app.forms import LoginForm, RegistrationForm, ActivitiesForm, SleepForm, ChildForm, FoodForm, DevelopmentalForm, IncidentForm, MedicationForm, NappyForm, NoteForm
from app.models import User, Nanny, Manager, Parent, Activity, Event, Sleep, Child, Food, Developmental, Incident, Medication, Nappy, Note
from flask_login import login_user, current_user, logout_user, login_required

@app.template_filter('format_date')
def format_date(event_time):
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    three_days_ago = yesterday - timedelta(days=2)
    
    if event_time.date() == today:
        return f"Today at {event_time.strftime('%H:%M')}"
    elif event_time.date() == yesterday:
        return f"Yesterday at {event_time.strftime('%H:%M')}"
    elif event_time.date() >= (three_days_ago):
        return event_time.strftime('%A')  # Format the day name using strftime
    else:
        return event_time .strftime('%d/%m/%y') # Return the original date for other cases

app.jinja_env.filters['format_date'] = format_date

def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn

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

def get_nanny_children(nanny, child_ids):
    if isinstance(child_ids, str):
        child_ids = [child_ids]  # Transform the single ID into a list

    return Child.query.filter(Child.child_id.in_(child_ids)).all()

@app.route('/')
@app.route('/index')
def index():
    current_id = current_user.user_id
    nanny = Nanny.query.filter_by(user_id=current_id).first()

    assigned_children = []
    for child in nanny.children:
        assigned_children.append(child.first_name) 

    print(assigned_children)
    events = Event.query.order_by(Event.event_time.desc()).all()
    return render_template('index.html', title='Home', events=events, now=datetime.now())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password')

    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data, 
            email=form.email.data, 
            role=form.role.data, 
            password=hashed_password)
        db.session.add(user)
        db.session.commit()

        
        if form.role.data == 'nanny':
            nanny = Nanny(
                user_id=user.user_id,
                manager_id=1
            )
            db.session.add(nanny)
            db.session.commit()

        
        if form.role.data == 'manager':
            manager = Manager(
                user_id=user.user_id,
            )
            db.session.add(manager)
            db.session.commit()



        flash("Your account has been created successfully. Please log in.")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/activities', methods=['GET', 'POST'])
@login_required
def activities():
    form = ActivitiesForm()
    current_id = current_user.user_id
    nanny = Nanny.query.filter_by(user_id=current_id).first()

    form.child.choices = [
        (child.child_id, f"{child.first_name} {child.last_name}") for child in nanny.children
    ]

    if form.validate_on_submit():
        children = get_nanny_children(nanny, form.child.data)
        event = Event(
            event_time=datetime.now(),
            event_type='Activities',
            user_id=current_id,
            children=children
        )
        db.session.add(event)
        db.session.commit()
        activity = Activity(
            duration=form.duration.data,
            description=form.description.data,
            picture=form.picture.data,
            event_id=event.event_id
        )
        db.session.add(activity)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('activities.html', title='Activities', 
    form=form)

@app.route('/developmental', methods=['GET', 'POST'])
@login_required
def developmental():
    form = DevelopmentalForm()

    current_id = current_user.user_id
    nanny = Nanny.query.filter_by(user_id=current_id).first()

    form.child.choices = [
        (child.child_id, f"{child.first_name} {child.last_name}") for child in nanny.children
    ]

    if form.validate_on_submit():
        children = get_nanny_children(nanny, form.child.data)
        event = Event(
            event_time=datetime.now(),
            event_type='Developmental',
            user_id=current_id,
            children=children
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
        return redirect(url_for('index'))
    return render_template('developmental.html', title='Developmental', form=form)
        


@app.route('/food', methods=['GET', 'POST'])
@login_required
def food():
    form = FoodForm()

    current_id = current_user.user_id
    nanny = Nanny.query.filter_by(user_id=current_id).first()

    form.child.choices = [
        (child.child_id, f"{child.first_name} {child.last_name}") for child in nanny.children
    ]

    if form.validate_on_submit():
        children = get_nanny_children(nanny, form.child.data)
        event = Event(
            event_time=datetime.now(),
            event_type='Food',
            user_id=current_id,
            children=children
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
    return render_template('food.html', title='Food', 
    form=form)

@app.route('/incident', methods=['GET', 'POST'])
@login_required
def incident():
    form = IncidentForm()

    current_id = current_user.user_id
    nanny = Nanny.query.filter_by(user_id=current_id).first()

    form.child.choices = [
        (child.child_id, f"{child.first_name} {child.last_name}") for child in nanny.children
    ]

    if form.validate_on_submit():
        children = get_nanny_children(nanny, form.child.data)
        event = Event(
            event_time=datetime.now(),
            event_type='Incident',
            user_id=current_id,
            children=children
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
    return render_template('incident.html', title='Incident', form=form)

@app.route('/medication', methods=['GET', 'POST'])
@login_required
def medication():
    form = MedicationForm()

    current_id = current_user.user_id
    nanny = Nanny.query.filter_by(user_id=current_id).first()

    form.child.choices = [
        (child.child_id, f"{child.first_name} {child.last_name}") for child in nanny.children
    ]

    if form.validate_on_submit():
        children = get_nanny_children(nanny, form.child.data)
        event = Event(
            event_time=datetime.now(),
            event_type='Medication',
            user_id=current_id,
            children=children
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
    return render_template('medication.html', title='Medication', form=form)

@app.route('/nappy', methods=['GET', 'POST'])
@login_required
def nappy():
    form = NappyForm()

    current_id = current_user.user_id
    nanny = Nanny.query.filter_by(user_id=current_id).first()

    form.child.choices = [
        (child.child_id, f"{child.first_name} {child.last_name}") for child in nanny.children
    ]

    if form.validate_on_submit():
        children = get_nanny_children(nanny, form.child.data)
        event = Event(
            event_time=datetime.now(),
            event_type='Nappy',
            user_id=current_id,
            children=children
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
    return render_template('nappy.html', title='Nappy', form=form)

@app.route('/note', methods=['GET', 'POST'])
@login_required
def note():
    form = NoteForm()

    current_id = current_user.user_id
    nanny = Nanny.query.filter_by(user_id=current_id).first()

    form.child.choices = [
        (child.child_id, f"{child.first_name} {child.last_name}") for child in nanny.children
    ]

    if form.validate_on_submit():
        children = get_nanny_children(nanny, form.child.data)
        event = Event(
            event_time=datetime.now(),
            event_type='Note',
            user_id=current_id,
            children=children
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
    return render_template('note.html', title='Note', form=form)

@app.route('/sleep', methods=['GET', 'POST'])
@login_required
def sleep():
    form = SleepForm()

    current_id = current_user.user_id
    nanny = Nanny.query.filter_by(user_id=current_id).first()

    form.child.choices = [
        (child.child_id, f"{child.first_name} {child.last_name}") for child in nanny.children
    ]

    if form.validate_on_submit():
        children = get_nanny_children(nanny, form.child.data)
        event = Event(
            event_time=datetime.now(),
            event_type='Sleep',
            user_id=current_id,
            children=children
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
    return render_template('sleep.html', title='Sleep', 
    form=form)

@app.route('/add_child', methods=['GET', 'POST'])
@login_required
def add_child():
    form = ChildForm()
    if form.validate_on_submit():
        if form.picture.data:
            print("working")
            picture_file = save_profile_picture(form.picture.data)
            child = Child(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                dob=form.dob.data,
                gender=form.gender.data,
                picture=picture_file
        )
        else:
            child = Child(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                dob=form.dob.data,
                gender=form.gender.data
            )
        db.session.add(child)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_child.html', title='Add Child', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

