from flask import render_template, url_for
from app import app
from app.main.forms import LoginForm


@app.route('/')
def home():  # put application's code here
    form = LoginForm()
    return render_template('login.html', title='Home', form=form)

