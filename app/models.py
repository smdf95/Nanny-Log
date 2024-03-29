from datetime import datetime
from itsdangerous import Serializer
from app import db, login_manager, app
from flask_login import UserMixin




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Company(db.Model):
    __tablename__ = 'companies'

    company_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Company %r>' % self.name



manager_child = db.Table('manager_child',
    db.Column('manager_id', db.Integer, db.ForeignKey('managers.manager_id')),
    db.Column('child_id', db.Integer, db.ForeignKey('children.child_id'))
)

manager_parent = db.Table('manager_parent',
    db.Column('manager_id', db.Integer, db.ForeignKey('managers.manager_id')),
    db.Column('parent_id', db.Integer, db.ForeignKey('parents.parent_id'))
)

manager_nanny = db.Table('manager_nanny',
    db.Column('manager_id', db.Integer, db.ForeignKey('managers.manager_id')),
    db.Column('nanny_id', db.Integer, db.ForeignKey('nannies.nanny_id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(64), index=True, nullable=False)
    last_name = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    picture = db.Column(db.String(20), nullable=True, default='default.png')
    role = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(128))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'))

    def get_reset_token(self, expiration_sec=1800):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.user_id, 'exp': expiration_sec})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token, expiration_sec=True)
            user_id = data.get('user_id')
        except:
            # Handle expired token
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.first_name}', {self.last_name}', '{self.email}', '{self.image_file}')"
    
    def get_id(self):
        return str(self.user_id)
    

class Manager(db.Model):
    __tablename__ = 'managers'

    manager_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    children = db.relationship('Child', secondary='manager_child', backref=db.backref('managers', lazy=True))
    parents = db.relationship('Parent', secondary='manager_parent', backref=db.backref('managers', lazy=True))
    nannies = db.relationship('Nanny', secondary='manager_nanny', backref=db.backref('managers', lazy=True))


    def __repr__(self):
        return f"Manager('{self.name}', '{self.company_id}')"
    
nanny_child = db.Table('nanny_child',
    db.Column('nanny_id', db.Integer, db.ForeignKey('nannies.nanny_id')),
    db.Column('child_id', db.Integer, db.ForeignKey('children.child_id'))
)
    
class Nanny(db.Model):
    __tablename__ = 'nannies'

    nanny_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.manager_id'))

    user = db.relationship('User', backref=db.backref('nanny', lazy=True), foreign_keys=[user_id])
    children = db.relationship('Child', secondary='nanny_child', backref=db.backref('nannies', lazy=True))

    def __repr__(self):
        children_names = ', '.join(child.first_name for child in self.children)
        return f"Nanny('{self.user.first_name}', '{self.nanny_id}', Children: '{children_names}')"
    
family = db.Table('family',
    db.Column('parent_id', db.Integer, db.ForeignKey('parents.parent_id')),
    db.Column('child_id', db.Integer, db.ForeignKey('children.child_id'))
)

class Parent(db.Model):
    __tablename__ = 'parents'

    parent_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.manager_id'))

    user = db.relationship('User', backref=db.backref('parent', lazy=True), foreign_keys=[user_id])
    children = db.relationship('Child', secondary=family, backref=db.backref('parents', lazy=True))

    def __repr__(self):
        children_names = ', '.join(child.first_name for child in self.children)
        return f"Parent('{self.user.first_name}', Children: '{children_names}')"
    
events_child = db.Table('events_child',
    db.Column('events_id', db.Integer, db.ForeignKey('events.event_id')),
    db.Column('child_id', db.Integer, db.ForeignKey('children.child_id'))
)

class Child(db.Model):
    __tablename__ = 'children'
    
    child_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    picture = db.Column(db.String(120), nullable=True, default='default.png')

    def __repr__(self):
        parents_names = ', '.join(parent.user.first_name for parent in self.parents)
        return f"Child('{self.first_name} {self.last_name}', Parents: '{parents_names}')"

class Activity(db.Model):
    __tablename__ = 'activities'

    activity_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    duration = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String(20), nullable=True)

    # Relationships
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))

class Developmental(db.Model):
    __tablename__ = 'developmentals'

    developmental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String(20), nullable=True)

    # Relationships
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))

class Food(db.Model):
    __tablename__ = 'foods'

    food_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meal_type = db.Column(db.String(9), nullable=False)
    description = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String(20), nullable=True)

    # Relationships
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))

class Incident(db.Model):
    __tablename__ = 'incidents'

    incident_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    incident_type = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Relationships
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))

class Medication(db.Model):
    __tablename__ = 'medications'

    medication_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    medication_name = db.Column(db.String(30), nullable=False)
    amount = db.Column(db.String(10), nullable=False)
    reason = db.Column(db.Text, nullable=True)
    time_given = db.Column(db.String(20), nullable=False)

    # Relationships
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))

class Nappy(db.Model):
    __tablename__ = 'nappies'

    nappy_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nappy_type = db.Column(db.String(5), nullable=False)
    condition = db.Column(db.String(100), nullable=True)

    # Relationships
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))

class Note(db.Model):
    __tablename__ = 'notes'

    note_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)

    # Relationships
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))


class Picture(db.Model):
    __tablename__ = 'pictures'

    picture_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    caption = db.Column(db.String(100), nullable=False)
    picture_file = db.Column(db.String(20), nullable=True)

    # Relationships
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))

class Sleep(db.Model):
    __tablename__ = 'sleeps'

    sleep_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sleep_start = db.Column(db.String, nullable=False)
    sleep_end = db.Column(db.String, nullable=False)

    # Relationships
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))

    



class Event(db.Model):
    __tablename__ = 'events'

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_time = db.Column(db.DateTime, nullable=False)
    event_type = db.Column(db.String(30), nullable=False)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    children = db.relationship('Child', secondary=events_child, backref=db.backref('events', lazy=True))


    activities = db.relationship("Activity", backref=db.backref('event', lazy=True))
    developmentals = db.relationship("Developmental", backref=db.backref('event', lazy=True))
    foods = db.relationship("Food", backref=db.backref('event', lazy=True))
    incidents = db.relationship("Incident", backref=db.backref('event', lazy=True))
    medications = db.relationship("Medication", backref=db.backref('event', lazy=True))
    nappies = db.relationship("Nappy", backref=db.backref('event', lazy=True))
    notes = db.relationship("Note", backref=db.backref('event', lazy=True))
    pictures = db.relationship("Picture", backref=db.backref('event', lazy=True))
    sleeps = db.relationship("Sleep", backref=db.backref('event', lazy=True))

class Comment(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment_time = db.Column(db.DateTime, nullable=False)
    comment_text = db.Column(db.String(255), nullable=False)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))