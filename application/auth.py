"""Routes for user authentication."""
from flask import redirect, render_template, flash, Blueprint, request, url_for
from flask_login import login_required, logout_user, current_user, login_user
from flask import current_app as app
from werkzeug.security import generate_password_hash
from .assets import compile_auth_assets
from .forms import LoginForm, SignupForm, CreatePlantForm, DeletePlantForm
from .models import db, User
from .import login_manager
from .models import Plants, Sensors, SensorInfo
from sqlalchemy.sql import select


# Blueprint Configuration
auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static')
compile_auth_assets(app)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    """User login page."""
    # Bypass Login screen if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('auth_bp.plantDashboardAuth'))
        #was main_bp.dashboard
    login_form = LoginForm(request.form)
    # POST: Create user and redirect them to the app
    if request.method == 'POST':
        if login_form.validate():
            # Get Form Fields
            email = request.form.get('email')
            password = request.form.get('password')
            # Validate Login Attempt
            user = User.query.filter_by(email=email).first()
            if user:
                if user.check_password(password=password):
                    login_user(user)
                    next = request.args.get('next')
                    return redirect(next or url_for('auth_bp.plantDashboardAuth')) #was main_bp.dashboard
        flash('Invalid username/password combination')
        return redirect(url_for('auth_bp.login_page'))
    # GET: Serve Log-in page
    return render_template('login.html',
                           form=LoginForm(),
                           title='Log in | Project GardenApp',
                           template='login-page',
                           body="Log in with your User account.")


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup_page():
    """User sign-up page."""

    signup_form = SignupForm(request.form)

    if request.method == 'POST':
        if signup_form.validate():
            # Get Form Fields
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            website = request.form.get('website')
            existing_user = User.query.filter_by(email=email).first()
            if existing_user is None:
                user = User(name=name,
                            email=email,
                            password=generate_password_hash(password, method='sha256'),
                            website=website)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('main_bp.dashboard'))
            flash('A user already exists with that email address.')
            return redirect(url_for('auth_bp.signup_page'))
    # GET: Serve Sign-up page
    return render_template('/signup.html',
                           title='Create an Account | Project GardenApp',
                           form=SignupForm(),
                           template='signup-page',
                           body="Sign up for a user account.")


@auth_bp.route('/plants', methods=['GET', 'POST'])
@login_required
def plantDashboardAuth():
    """Provide plant dashboard"""

    plantListDisplay = Plants.query.filter_by(userID=current_user.id)
    #plantListDisplay = db.query(Plants).filter_by(userID=current_user.id)
    create_plant = CreatePlantForm(request.form)
    delete_plant = DeletePlantForm(request.form)

    if request.method == 'POST':
        if delete_plant.validate():
            userinput = request.form.get('plantName1')
            userID = current_user.id

            #obj = Plants.query.filter_by(plantName=plantName1)
            #obj = db.session.execute('SELECT userID, plantName, plantType, plantThirst, sensorID FROM plants WHERE plantName =  \'%s\'' % plantName1)
            #userinput = "Delete Me 1"

            #submit data to DB
            #db.session.delete(obj)
            flash('TESTING !23')
            flash(userinput)
            app.logger.info(userinput)
            db.session.query(Plants).filter(plantName=userinput).delete()
            db.session.commit()
            flash('Your plant was deleted!')

            #reload the page
            return redirect(url_for('auth_bp.plantDashboardAuth'))

        if create_plant.validate():
            plantName = request.form.get('plantName')
            plantType = request.form.get('plantType')
            plantThirst = request.form.get('plantThirst')
            sensorID = request.form.get('sensorID')

            #create plant object
            plant = Plants(userID=current_user.id,
                           plantName=plantName,
                           plantType=plantType,
                           plantThirst=plantThirst,
                           sensorID=sensorID)

            #submit data to DB
            db.session.add(plant)
            db.session.commit()
            flash('Your plant was added!')

            #reload the page
            return redirect(url_for('auth_bp.plantDashboardAuth'))



    return render_template('plants.html',
                           title='Plant Dashboard | Project GardenApp',
                           template='dashboard-template',
                           current_user=current_user,
                           form=CreatePlantForm(),
                           plants=plantListDisplay,
                           body="",
                           userID=(current_user.id))





@auth_bp.route('/plantinfo', methods=['GET'])
@login_required
def notificationList():
    """Notification and Plant Setting Page"""

    query1 = db.session.query(Plants, SensorInfo).outerjoin(SensorInfo, Plants.sensorID == SensorInfo.sensorID).all()

    query2 = db.session.execute('SELECT p.sensorID, p.plantName, s.moistRead, s.sensorTime FROM plants p, sensorInfo s WHERE p.sensorID = s.sensorID ORDER BY s.sensorTime DESC LIMIT 5;')

    return render_template('plantinfo.html',
                           title='Sensor Info | Project GardenApp',
                           template='dashboard-template',
                           current_user=current_user,
                           body="Moisture reading is displayed at each time a reading was taken.",
                           display=query2)


@auth_bp.route("/logout")
@login_required
def logout_page():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login_page'))


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login_page'))
