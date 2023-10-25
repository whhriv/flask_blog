from app import app, db
from flask import render_template, redirect, url_for, flash
# Import the SingUpForm and LoginForm class from forms
from app.forms import SignUpForm, LoginForm
# Import the User model from models
from app.models import User

# Create our first route
@app.route('/')
def index():
    return render_template('index.html')

# Create a second route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Create an instance of the SignUpForm
    form = SignUpForm()
    if form.validate_on_submit():
        # Get the data from each of the fields
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # print(first_name, last_name, username, email, password)

        # Check to see if we already have a User with that username or email
        check_user = db.session.execute(db.select(User).where( (User.username==username) | (User.email==email) )).scalars().all()
        if check_user:
            flash('A user with that username and/or email already exists')
            return redirect(url_for('signup'))
        # Create a new instance of the User class with the data from the form
        new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        # Add the new user object to the database
        db.session.add(new_user)
        db.session.commit()

        flash(f"{new_user.username} has been created!")

        # Redirect back to the home page
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


@app.route('/login')
def login():
    # Create an instance of the LoginForm
    form = LoginForm()
    return render_template('login.html', form=form)
