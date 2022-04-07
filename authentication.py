from flask import render_template, flash, redirect, url_for
from app import db
from app.main.forms import LoginForm, SignUpForm
from flask_login import login_user, current_user
from app.models import User


def do_login(the_current_user):
    """
    This method authenticates and logs users in.
    :param the_current_user: The user object returned by the query.
    :return: The user is logged into their profile and redirected to the home page.
    """
    # current_user is a global variable provided by the flask_login module
    if the_current_user.is_authenticated:
        return redirect(url_for('show_home'))
    form = LoginForm()  # Create a LoginForm object from forms.py
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.emailAddress.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash("Logged in as: " + str(form.emailAddress.data), 'success')
        return redirect(url_for('show_home'))
    return render_template('authorization/logIn.html', title='Log In', form=form)


def do_sign_up():
    """
    This method creates a user object.
    :return: A redirect to the login page with a successful sign up.
    """
    if current_user.is_authenticated:
        return redirect(url_for('show_home'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.firstName.data, email=form.emailAddress.data, first_name=form.firstName.data,
                    last_name=form.lastName.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Account created for: " + str(form.emailAddress.data), 'success')
        return redirect(url_for('login'))
    return render_template('authorization/sign_Up.html', title='Sign Up', form=form)
