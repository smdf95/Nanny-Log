import os
import secrets
from PIL import Image
from flask import render_template, request, redirect, url_for, flash, Blueprint
from app import app, db, bcrypt, login_manager
from app.forms import LoginForm, RegistrationForm, ChildForm, AssignChild, UpdateProfileForm
from app.models import User, Nanny, Parent, Manager, Parent, Child, Event
from flask_login import login_user, current_user, logout_user, login_required

main_blueprint = Blueprint('main', __name__)



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
        return redirect(url_for('login'))
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

@main_blueprint.route('/child_profile/<int:child_id>')
def child_profile(child_id):
    page = request.args.get('page', 1, type=int)
    kid = Child.query.get_or_404(child_id)
    events = Event.query.filter_by(child_id=kid.child_id)\
                    .order_by(Event.event_time.desc())\
                    .paginate(page=page, per_page=10)
    return render_template('child_profile.html', title=kid.first_name, events=events, child=kid)