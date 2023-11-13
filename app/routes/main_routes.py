import os
import secrets
from datetime import date
from PIL import Image
from functools import wraps
from flask import render_template, request, redirect, url_for, flash, Blueprint, abort
from app import app, db, bcrypt, login_manager
from app.forms import LoginForm, RegistrationForm, ChildForm, AssignChild, UpdateProfileForm
from app.models import User, Nanny, Parent, Manager, Parent, Child, Event, Activity, Food, Incident, Developmental, Nappy, Note, Sleep, Medication
from flask_login import login_user, current_user, logout_user, login_required

main_blueprint = Blueprint('main', __name__)

from functools import wraps
from flask import abort
from flask_login import current_user

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

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn



def get_assigned_children(user, child_ids):
    if isinstance(child_ids, str):
        child_ids = [child_ids]  # Transform the single ID into a list

    return Child.query.filter(Child.child_id.in_(child_ids)).all()

def get_assigned_parents(user, parent_ids):
    if isinstance(parent_ids, str):
        parent_ids = [parent_ids]  # Transform the single ID into a list

    return Parent.query.filter(Parent.parent_id.in_(parent_ids)).all()

def get_assigned_nannies(user, nanny_ids):
    if isinstance(nanny_ids, str):
        nanny_ids = [nanny_ids]  # Transform the single ID into a list

    return Nanny.query.filter(Nanny.nanny_id.in_(nanny_ids)).all()



        
    

@main_blueprint.route('/login', methods=['GET', 'POST'])
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

@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        manager = Manager.query.filter_by(manager_id=1).first()
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
            nanny.managers.append(manager)
            
            db.session.add(nanny)
            db.session.commit()
        elif form.role.data == 'parent':
            parent = Parent(
                user_id=user.user_id,
                manager_id=1
            )
            parent.managers.append(manager)
            db.session.add(parent)
            db.session.commit()
        
        
        elif form.role.data == 'manager':
            manager = Manager(
                user_id=user.user_id,
            )
            db.session.add(manager)
            db.session.commit()



        flash("Your account has been created successfully. Please log in.")
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main_blueprint.route('/assign_child', methods=['GET', 'POST'])
@login_required
def assign_child():
    form = AssignChild()
    current_id = current_user.user_id

    manager = Manager.query.filter_by(user_id=current_id).first()
    parents = db.session.query(Parent, User).\
    join(User, Parent.user_id == User.user_id).\
    filter(Parent.manager_id == manager.manager_id).all()
    nannies = db.session.query(Nanny, User).\
    join(User, Nanny.user_id == User.user_id).\
    filter(Nanny.manager_id == manager.manager_id).all()


    form.child.choices = [
        (child.child_id, f"{child.first_name} {child.last_name}") for child in manager.children
    ]
    initial_parent_choice = (None, "Please Select a Parent (if necessary)")
    parent_choices = [
        (parent.parent_id, f"{user.first_name} {user.last_name}") for parent, user in parents
    ]
    parent_choices.insert(0, initial_parent_choice)
    form.parent.choices = parent_choices
    initial_nanny_choice = (None, "Please Select a Nanny (if necessary)")
    nanny_choices = [
        (nanny.nanny_id, f"{user.first_name} {user.last_name}") for nanny, user in nannies
    ]
    nanny_choices.insert(0, initial_nanny_choice)
    form.nanny.choices = nanny_choices

    if form.validate_on_submit():
        child_id = form.child.data
        child = Child.query.filter_by(child_id=child_id).first()
        if form.parent.data is not None and form.parent.data != 'None':
            parents = get_assigned_parents(manager, form.parent.data)
            for parent in parents:
                child.parents.append(parent)

        elif form.nanny.data is not None and form.nanny.data != 'None':
            nannies = get_assigned_nannies(manager, form.nanny.data)
            for nanny in nannies:
                child.nannies.append(nanny)
        
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('assign_child.html', title='Assign Child', form=form)

@main_blueprint.route('/add_child', methods=['GET', 'POST'])
@login_required
def add_child():
    form = ChildForm()
    current_id = current_user.user_id
    manager = Manager.query.filter_by(user_id=current_id).first()

    if form.validate_on_submit():
        if form.picture.data:
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
                gender=form.gender.data,
                picture="default.png"
            )
        child.managers.append(manager)
        db.session.add(child)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_child.html', title='Add Child', form=form)

@main_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@main_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    user_image = url_for('static', filename='profile_pics/' + current_user.picture)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_profile_picture(form.picture.data)
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
            current_user.picture = picture_file
        else:
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    return render_template('profile.html', title='Profile', form=form, user_image=user_image)

@main_blueprint.route('/view_profiles', methods=['GET', 'POST'])
@login_required
def view_profiles():
    current_id = current_user.user_id
    manager = Manager.query.filter_by(user_id=current_id).first()
    return render_template('view_profiles.html', title='View Profiles', manager=manager)

def calculateAge(birthDate): 
    today = date.today()
    age_years = today.year - birthDate.year - ((today.month, today.day) <  (birthDate.month, birthDate.day)) 
    age_months = today.month - birthDate.month
    if age_years > 0:
        if age_months < 0:
            age_years -=1
            age_months += 12
    elif age_years == 0:
        if age_months < 0:
            age_months += 12
    if age_years == 1:
        if age_months == 1:
            return str(age_years) + " year " + str(age_months) + " month"
        else:
            return str(age_years) + " year " + str(age_months) + " months"
    else:
        if age_months == 1:
            return str(age_years) + " years " + str(age_months) + " month"
        else:
            return str(age_years) + " years " + str(age_months) + " months"
   

@main_blueprint.route('/child_profile/<int:child_id>')
@login_required
@association_required
def child_profile(child_id):
    page = request.args.get('page', 1, type=int)
    kid = Child.query.get_or_404(child_id)
    age = calculateAge(kid.dob)
    events = Event.query.filter_by(child_id=kid.child_id)\
                    .order_by(Event.event_time.desc())\
                    .paginate(page=page, per_page=10)
    return render_template('child_profile.html', title=kid.first_name, events=events, child=kid, age=age)

@main_blueprint.route('/remove_parent_association/<int:child_id>/<int:parent_id>')
@login_required
@manager_required
def remove_parent_association(child_id, parent_id):
    child = Child.query.get_or_404(child_id)
    parent = Parent.query.get_or_404(parent_id)
    child.parents.remove(parent)
    db.session.commit()
    flash('Parent removed from child')
    return redirect(url_for('main.child_profile', child_id=child_id))

@main_blueprint.route('/remove_nanny_association/<int:child_id>/<int:nanny_id>')
@login_required
@manager_required
def remove_nanny_association(child_id, nanny_id):
    child = Child.query.get_or_404(child_id)
    nanny = Nanny.query.get_or_404(nanny_id)
    child.nannies.remove(nanny)
    db.session.commit()
    flash('Nanny removed from child')
    return redirect(url_for('main.child_profile', child_id=child_id))

@main_blueprint.route('/remove_child/<int:child_id>')
@login_required
@manager_required
def remove_child(child_id):
    events = Event.query.filter_by(child_id=child_id).all()
    for event in events:
        activities = Activity.query.filter_by(event_id=event.event_id).all()
        developmentals = Developmental.query.filter_by(event_id=event.event_id).all()
        foods = Food.query.filter_by(event_id=event.event_id).all()
        incidents = Incident.query.filter_by(event_id=event.event_id).all()
        medications = Medication.query.filter_by(event_id=event.event_id).all()
        nappies = Nappy.query.filter_by(event_id=event.event_id).all()
        notes = Note.query.filter_by(event_id=event.event_id).all()
        sleeps = Sleep.query.filter_by(event_id=event.event_id).all()
        if activities:
            Activity.query.filter_by(event_id=event.event_id).delete()
        if developmentals:
            Developmental.query.filter_by(event_id=event.event_id).delete()
        if foods:
            Food.query.filter_by(event_id=event.event_id).delete()
        if incidents:
            Incident.query.filter_by(event_id=event.event_id).delete()
        if medications:
            Medication.query.filter_by(event_id=event.event_id).delete()
        if nappies:
            Nappy.query.filter_by(event_id=event.event_id).delete()
        if notes:
            Note.query.filter_by(event_id=event.event_id).delete()
        if sleeps:
            Sleep.query.filter_by(event_id=event.event_id).delete()
        
        Event.query.filter_by(event_id=event.event_id).delete()
    
    Child.query.filter_by(child_id=child_id).delete()
    
    db.session.commit()
    flash('Child removed from database')
    return redirect(url_for('index'))

@main_blueprint.route('/remove_user/<int:user_id>')
@login_required
@manager_required
def remove_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if user.role == 'nanny':
        Nanny.query.filter_by(user_id=user_id).delete()
    elif user.role == 'parent':
        Parent.query.filter_by(user_id=user_id).delete()
    
    User.query.filter_by(user_id=user_id).delete()
    
    db.session.commit()
    flash('User removed from database')
    return redirect(url_for('index'))

@main_blueprint.route('/others_profile/<int:user_id>')
@login_required
def others_profile(user_id):
    user = User.query.get_or_404(user_id)
    nanny = Nanny.query.filter_by(user_id=user_id).first()
    parent = Parent.query.filter_by(user_id=user_id).first()
    return render_template('others_profile.html', user=user, nanny=nanny, parent=parent)
