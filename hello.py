import os

from flask import Flask, render_template, session, flash, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, ValidationError
from wtforms.validators import DataRequired, Email
from datetime import datetime, UTC
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback_key')

def uoft_email_check(_, field):
    if not field.data.endswith('utoronto.ca'):
        raise ValidationError('Email must be from the utoronto.ca domain.')

class StudentForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = EmailField('What is your email?', validators=[DataRequired(), Email(), uoft_email_check])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = StudentForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you changed your name!')
        old_email = session.get('email')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you changed your email!')
        session['email'] = form.email.data
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, current_time=datetime.now(UTC))

@app.errorhandler(404) 
def page_not_found(e): 
    return render_template('404.html'), 404 

@app.errorhandler(500) 
def internal_server_error(e): 
    return render_template('500.html'), 500