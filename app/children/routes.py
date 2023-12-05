from flask import (
    render_template, 
    request, 
    redirect, 
    url_for, 
    flash, 
    Blueprint
)
from flask_login import current_user, login_required
from app import db
from app.children.forms import ChildForm, AssignChild, EditProfileForm
from app.models import (
    User, 
    Nanny, 
    Parent,
    Manager, 
    Child, 
    Event, 
    Activity, 
    Food, 
    Incident, 
    Developmental, 
    Nappy, 
    Note, 
    Sleep, 
    Medication
)
from .utils import (
    save_profile_picture, 
    get_assigned_nannies, 
    get_assigned_parents, 
    manager_required, 
    association_required, 
    calculate_age, 
    get_assigned_children
)
from sqlalchemy import text


children_blueprint = Blueprint('children', __name__)


@children_blueprint.route('/assign_child', methods=['GET', 'POST'])
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

    form.parent.choices = [
        (parent.parent_id, f"{parent.user.first_name} {parent.user.last_name}") for parent in manager.parents
    ]

    form.nanny.choices = [
        (nanny.nanny_id, f"{nanny.user.first_name} {nanny.user.last_name}") for nanny in manager.nannies
    ]

    if request.method == 'POST':
        if form.validate_on_submit():
            selected_child_ids = form.child.data
            selected_children = get_assigned_children(selected_child_ids)
            for child in selected_children:
                if form.parent.data is not None and form.parent.data != 'None':
                    parents = get_assigned_parents(manager, form.parent.data)
                    for parent in parents:
                        if parent not in child.parents:
                            child.parents.append(parent)
                        else:
                            pass
                    
                    if form.nanny.data is not None and form.nanny.data != 'None':
                        nannies = get_assigned_nannies(manager, form.nanny.data)
                        for nanny in nannies:
                            if nanny not in child.nannies:
                                child.nannies.append(nanny)
                            else:
                                pass

                elif form.nanny.data is not None and form.nanny.data != 'None':
                    nannies = get_assigned_nannies(manager, form.nanny.data)
                    for nanny in nannies:
                        child.nannies.append(nanny)


        
        db.session.commit()

        if len(selected_child_ids) == 1:
            return redirect(url_for('children.child_profile', child_id=selected_child_ids[0]))
        else: 
            return redirect(url_for('users.view_profiles'))


    return render_template('children/assign_child.html', title='Assign Child', form=form, Child=Child, User=User, Nanny=Nanny, Parent=Parent)

@children_blueprint.route('/add_child', methods=['GET', 'POST'])
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
    return render_template('children/add_child.html', title='Add Child', form=form)



@children_blueprint.route('/child_profile/<int:child_id>')
@login_required
@association_required
def child_profile(child_id):
    page = request.args.get('page', 1, type=int)
    kid = Child.query.get_or_404(child_id)
    age = calculate_age(kid.dob)
    
    events = Event.query\
        .join(Event.children)\
        .filter(Child.child_id == kid.child_id)\
        .order_by(Event.event_time.desc())\
        .paginate(page=page, per_page=10)
    
    return render_template('children/child_profile.html', title=kid.first_name, events=events, child=kid, age=age)

@children_blueprint.route('/remove_parent_association/<int:child_id>/<int:parent_id>/<next>')
@login_required
@manager_required
def remove_parent_association(child_id, parent_id, next):
    child = Child.query.get_or_404(child_id)
    parent = Parent.query.get_or_404(parent_id)
    child.parents.remove(parent)
    db.session.commit()
    if next == 'parent':
        flash('Child removed from parent')
        return redirect(url_for('users.others_profile', user_id=parent.user_id))
    else:
        flash('Parent removed from child')
        return redirect(url_for('children.child_profile', child_id=child.child_id))

@children_blueprint.route('/remove_nanny_association/<int:child_id>/<int:nanny_id>/<next>')
@login_required
@manager_required
def remove_nanny_association(child_id, nanny_id, next):
    child = Child.query.get_or_404(child_id)
    nanny = Nanny.query.get_or_404(nanny_id)
    child.nannies.remove(nanny)
    db.session.commit()
    if next == 'nanny':
        flash('Child removed from nanny')
        return redirect(url_for('users.others_profile', user_id=nanny.user_id))
    else:
        flash('Nanny removed from child')
        return redirect(url_for('children.child_profile', child_id=child.child_id))

@children_blueprint.route('/remove_child/<int:child_id>')
@login_required
@manager_required
def remove_child(child_id):
    events = Event.query\
            .join(Event.children)\
            .filter_by(child_id=child_id)
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


    db.session.execute(
            text("DELETE FROM manager_child WHERE child_id = :child_id"),
            {"child_id": child_id}
        )
    db.session.execute(
            text("DELETE FROM family WHERE child_id = :child_id"),
            {"child_id": child_id}
        )
    db.session.execute(
            text("DELETE FROM nanny_child WHERE child_id = :child_id"),
            {"child_id": child_id}
        )
    
    Child.query.filter_by(child_id=child_id).delete()
    
    db.session.commit()
    flash('Child removed from database')
    return redirect(url_for('index'))

@children_blueprint.route('/edit_profile/<int:child_id>', methods=['GET', 'POST'])
def edit_profile(child_id):
    form = EditProfileForm()
    child = Child.query.filter_by(child_id=child_id).first()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_profile_picture(form.picture.data)
            child.first_name = form.first_name.data
            child.last_name = form.last_name.data
            child.dob = form.dob.data
            child.gender = form.gender.data
            child.picture = picture_file
        else:
            child.first_name = form.first_name.data
            child.last_name = form.last_name.data
            child.dob = form.dob.data
            child.gender = form.gender.data
        db.session.commit()
        return redirect(url_for('children.child_profile', child_id=child.child_id))
    elif request.method == 'GET':
        form.first_name.data = child.first_name
        form.last_name.data = child.last_name
        form.dob.data = child.dob
        form.gender.data = child.gender
    return render_template('children/edit_profile.html', title='Edit Child Profile', form=form)

@children_blueprint.route('/my_kids')
@login_required
def my_kids():
    """
    This function renders the page with all the children that the logged in user has.
    """
    nanny = Nanny.query.filter_by(user_id=current_user.user_id).first()
    parent = Parent.query.filter_by(user_id=current_user.user_id).first()
    return render_template('children/my_kids.html', title='My Kids', nanny=nanny, parent=parent)
