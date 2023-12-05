import os
from datetime import datetime, timedelta

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from flask_mail import Mail




app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('DB_EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('DB_PASS')
mail = Mail(app)


from app.models import Nanny, Parent, Manager, Parent, Event, Child
from .events.routes import events_blueprint
from .children.routes import children_blueprint
from .users.routes import users_blueprint
app.register_blueprint(events_blueprint)
app.register_blueprint(children_blueprint)
app.register_blueprint(users_blueprint)

@app.template_filter('format_date')
def format_date(event_time):
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    three_days_ago = yesterday - timedelta(days=2)
    
    if event_time.date() == today:
        return f"{event_time.strftime('%H:%M')}"
    elif event_time.date() == yesterday:
        return f"Yesterday at {event_time.strftime('%H:%M')}"
    elif event_time.date() >= (three_days_ago):
        return event_time.strftime('%A')  # Format the day name using strftime
    else:
        return event_time.strftime('%d/%m/%y') # Return the original date for other cases

app.jinja_env.filters['format_date'] = format_date

@app.route('/')
@app.route('/index')
def index():
    
    if current_user.is_authenticated:

        current_id = current_user.user_id
        child_ids = []

        if current_user.role == 'nanny':
            nanny = Nanny.query.filter_by(user_id=current_id).first()
            if nanny:
                child_ids = [child.child_id for child in nanny.children]
        elif current_user.role == 'manager':
            manager = Manager.query.filter_by(user_id=current_id).first()
            if manager:
            
                child_ids = [child.child_id for child in manager.children]
        elif current_user.role == 'parent':
            parent = Parent.query.filter_by(user_id=current_id).first()
            if parent:

                child_ids = [child.child_id for child in parent.children]

        page = request.args.get('page', 1, type=int)
        print(child_ids)
        
        events = Event.query\
            .join(Event.children)\
            .filter(Child.child_id.in_(child_ids))\
            .order_by(Event.event_time.desc())\
            .paginate(page=page, per_page=15)

        print("events:", events.items) 
        for event in events:
            print(event.children)

        return render_template('index.html', title='Home', events=events, now=datetime.now())
    
    else:
        return render_template('index.html', title='Home', now=datetime.now())
