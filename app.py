from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user  # for user profile dashboard in side corner
from flask_login import login_required
from connectDB import db, Community, Activity
from integrateMail import mail, configure_mail
from flask_mail import Message
from flask_migrate import Migrate
from sqlalchemy.orm import joinedload


app = Flask(__name__)
app.secret_key = "your‑secret‑key"           # needed for session cookies
configure_mail(app)

# MySQL database connection config
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost:3307/project1"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)
@app.route('/')
def home():
    # Fetch all activities (newest first), eager‑load the Community (poster)
    feed = Activity.query \
        .options(joinedload(Activity.user)) \
        .order_by(Activity.date.desc()) \
        .all()
    return render_template('index.html', feed=feed)


@app.route('/notices')
def notices():
    return render_template('notices.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Community.query.filter_by(
            email=request.form['email'].strip()
        ).first()
        if user and user.password == request.form['password'].strip():
            login_user(user)
            return redirect(url_for('home'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        # Handle signup logic here
        return redirect(url_for('login'))

    return render_template('signup.html')

# ⭐
@app.route('/submit',methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    new_member = Community(name=name, email=email, password=password)

    # Add to DB session and commit
    db.session.add(new_member)
    db.session.commit()
    msg="Your account has been created successfully!"
    return render_template('signup.html',msg=msg)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mail1 = request.form['message']

        # from flask_mail import Message
        msg = Message(
            "Mail from Community member",
            sender=email,
            recipients=['arpit.2428cseai2125@kiet.edu']  # or your own email
        )
        msg.body = f"From: {name} <{email}>\n\n{mail1}"
        # msg.body=f"From: {name} "
        mail.send(msg)
        return render_template('contact.html',msg="Your message has been sent successfully!")
    return render_template("contact.html")


@app.route('/about')
def about():
    return render_template('about.html')

# Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"          # @login_required redirects here



@app.route('/dashboard')
@login_required
def dashboard():
    # pull all activities for this user, newest first
    activities = Activity.query \
        .filter_by(user_id=current_user.id) \
        .order_by(Activity.date.desc()) \
        .all()
    return render_template('dashboard.html', activities=activities)


@login_manager.user_loader
def load_user(user_id):
    return Community.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/activity/edit/<int:activity_id>', methods=['GET','POST'])
@login_required
def edit_activity(activity_id):
    act = Activity.query.get_or_404(activity_id)
    if act.user_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        act.notice = request.form.get('notice')
        act.event  = request.form.get('event')
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('edit_activity.html', activity=act)

@app.route('/activity/delete/<int:activity_id>')
@login_required
def delete_activity(activity_id):
    act = Activity.query.get_or_404(activity_id)
    if act.user_id != current_user.id:
        abort(403)
    db.session.delete(act)
    db.session.commit()
    return redirect(url_for('dashboard'))


from connectDB import Activity
# Creating a new notice
@app.route('/notices/new', methods=['GET','POST'])
@login_required
def new_notice():
    if request.method == 'POST':
        notice_text = request.form['notice']
        # record in Activity
        act = Activity(user_id=current_user.id,
                       notice=notice_text,
                       event=None)
        db.session.add(act)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('new_notice.html')


@app.route('/events/new', methods=['GET','POST'])
@login_required
def new_event():
    if request.method == 'POST':
        event_text = request.form['event']
        act = Activity(user_id=current_user.id,
                       notice=None,
                       event=event_text)
        db.session.add(act)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('new_event.html')





if __name__ == '__main__':
    app.run(debug=True)

