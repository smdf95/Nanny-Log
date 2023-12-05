from flask import (
    render_template, 
    request, 
    redirect, 
    url_for, 
    flash, 
    Blueprint
)
from flask_login import (
    login_user, 
    current_user, 
    logout_user, 
    login_required
)
from app import db, bcrypt
from app.models import User, Nanny, Parent, Manager, Child
from app.users.forms import (
    LoginForm, 
    RegistrationForm, 
    UpdateProfileForm, 
    ResetPasswordForm, 
    RequestResetForm, 
    ChangePasswordForm
)
from app.users.utils import (
    save_profile_picture, 
    send_reset_email, 
    manager_required
)
from sqlalchemy import text



users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/login', methods=['GET', 'POST'])
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

    return render_template('users/login.html', title='Login', form=form)

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        managers = Manager.query.all()
        parents = Parent.query.all()
        nannies = Nanny.query.all()
        children = Child.query.all()
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
            )
            for manager in managers:
                nanny.managers.append(manager)
            
            db.session.add(nanny)
            db.session.commit()
        elif form.role.data == 'parent':
            parent = Parent(
                user_id=user.user_id,
            )
            for manager in managers:
                parent.managers.append(manager)
            db.session.add(parent)
            db.session.commit()
        
        
        elif form.role.data == 'manager':
            manager = Manager(
                user_id=user.user_id,
            )
            for parent in parents:
                manager.parents.append(parent)
            for nanny in nannies:
                manager.nannies.append(nanny)
            for child in children:
                manager.children.append(child)
            db.session.add(manager)
            db.session.commit()



        flash("Your account has been created successfully. Please log in.")
        return redirect(url_for('users.login'))
    return render_template('users/register.html', title='Register', form=form)



@users_blueprint.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('users/forgot_password.html', title='Forgot Password', form=form)

@users_blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token')
        return redirect(url_for('users.forgot_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in')
        return redirect(url_for('users.login'))
    return render_template('users/reset_password.html', title='Reset Password', form=form)


@users_blueprint.route('/change_password/<int:user_id>', methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    if current_user.user_id != user_id:
        flash("Cannot change other's passwords")
        return redirect(url_for('index'))
    form = ChangePasswordForm()
    user = User.query.get(user_id)
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
        if user and bcrypt.check_password_hash(user.password, form.old_password.data):
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated!')
        else:
            flash("Password is incorrect")
    return render_template('users/change_password.html', form=form)

@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@users_blueprint.route('/profile', methods=['GET', 'POST'])
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
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    return render_template('users/profile.html', title='Profile', form=form, user_image=user_image)

@users_blueprint.route('/view_profiles', methods=['GET', 'POST'])
@login_required
def view_profiles():
    current_id = current_user.user_id
    manager = Manager.query.filter_by(user_id=current_id).first()
    return render_template('users/view_profiles.html', title='View Profiles', manager=manager)

@users_blueprint.route('/remove_user/<int:user_id>')
@login_required
@manager_required
def remove_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if user.role == 'nanny':
        nanny = Nanny.query.filter_by(user_id=user_id).first()
        db.session.execute(
            text("DELETE FROM manager_nanny WHERE nanny_id = :nanny_id"),
            {"nanny_id": nanny.nanny_id}
        )
        Nanny.query.filter_by(user_id=user_id).delete()
    elif user.role == 'parent':
        parent = parent.query.filter_by(user_id=user_id).first()
        db.session.execute(
            text("DELETE FROM manager_parent WHERE parent_id = :parent_id"),
            {"parent_id": parent.parent_id}
        )
        Parent.query.filter_by(user_id=user_id).delete()
    
    User.query.filter_by(user_id=user_id).delete()
    
    db.session.commit()
    flash('User removed from database')
    return redirect(url_for('index'))

@users_blueprint.route('/others_profile/<int:user_id>')
@login_required
def others_profile(user_id):
    user = User.query.get_or_404(user_id)
    nanny = Nanny.query.filter_by(user_id=user_id).first()
    manager = Manager.query.filter_by(user_id=user_id).first()
    parent = Parent.query.filter_by(user_id=user_id).first()
    current_nanny = Nanny.query.filter_by(user_id=current_user.user_id).first()
    current_parent = Parent.query.filter_by(user_id=current_user.user_id).first()
    return render_template('users/others_profile.html', user=user, manager=manager, nanny=nanny, parent=parent, current_nanny=current_nanny, current_parent=current_parent, next=next)

    