from flask import render_template, url_for, flash, redirect, request
from app import application, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, ControlPanelForm
from app.models import User, Testimonial
from flask_login import login_user, current_user, logout_user, login_required

testimonials = [
    {
        'topic': 'Samajik Suraksha Yojana',
        'description': 'Social security for unorganised workers',
        'writeup': 'The West Bengal Labour Welfare Board is a statutory and autonomous body.',
        'author': 'Priyanko Banerjee',
        'date': 'August 20, 2018'
    },
    {
        'topic': 'Fluxionbits',
        'description': 'Solutions that create impact',
        'writeup': 'Custom Apps, Integration Services and Staffing Solutions',
        'author': 'Rakesh Mallick',
        'date': 'August 22, 2018'
    }
]

@application.route("/")
@application.route("/home")
def home():
    return render_template('home.html', posts=testimonials)

@application.route("/about")
def about():
    return render_template('about.html', title='About')

@application.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))        
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}. You can now login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@application.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@application.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@application.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has been update!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email 
    img_file = url_for('static', filename='profile_pics/' + current_user.img_file)
    return render_template('account.html', title='Account', img_file=img_file, form=form)


@application.route("/analytics", methods=['GET', 'POST'])
def analytics():
    form = ControlPanelForm()
    return render_template('analytics.html', title='Analytics', form=form)
