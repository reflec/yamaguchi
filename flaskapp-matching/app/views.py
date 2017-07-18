from flask import render_template, flash ,redirect ,session,url_for,request,g
from flask import Flask,jsonify
import json
from flask_login import login_user,logout_user,current_user, login_required
from flask_msearch import Search
from app import app,db, lm
from .forms import LoginForm,EditForm,SearchForm,RegistrationForm,CalendarForm,DayForm
from .models import User,Day
from datetime import datetime
from config import MAX_SEARCH_RESULTS
from app import babel
from config import LANGUAGES

import flask_whooshalchemy as whooshalchemy

from flask_msearch import Search





@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form= SearchForm()

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'),500

@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
def index():
    return render_template('index.html',title='Home')




@app.route('/resister',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
        nickname=form.nickname.data,
        password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html',title='Sign In',form=form)

def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname,email=resp.email)
        db.session.add(user)
        db.session.commit()

    remember_me = False
    if 'remember_me' in session:
        remember_me = session('remember_me')
        session.pop('remember_me',None)
    login_user(user,remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    return render_template('user.html',
                          user=user)


@app.route('/edit',methods=['GET','POST'])
@login_required
def edit():
    form= EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        g.user.gender = form.gender.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))

    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me

    dform = DayForm()
    if dform.validate_on_submit():
        day = Day(possible_day=dform.possible_day.data,author=g.user)
        db.session.add(day)
        db.session.commit()
        whooshalchemy.whoosh_index(app, Day)
        return redirect(url_for('edit'))
    days = Day(possible_day=dform.possible_day.data,author=g.user)

    return render_template('edit.html',form=form,dform=dform,days=days)








    form = CalendarForm()
    if form.validate_on_submit():
        day = Day(body=form.day.data,)
        db.session.add(day)
        db.session.commit()
        whooshalchemy.whoosh_index(app, Day)
        return redirect(url_for('index'))

    return render_template("json.html")

    title_data = request.args.get('title', '')
    start_date = request.args.get('star', '')
    end_date = request.args.get('end', '')

    with open("events.json", "r") as input_data:
        return input_data.read()







@app.route('/search',methods=['POST'])
@login_required
def search():
#    if not g.search_form.validate_on_submit():
#        return redirect(url_for('index'))
    return redirect(url_for('search_results',query=g.search_form.search.data))


@app.route('/searchpage',methods=['GET','POST'])
def searchpage():
    return render_template('searchpage.html',title='seachpage')


@app.route('/search_results/<query>')
def search_results(query):

    search = Search()
    search.init_app(app)
    whooshalchemy.whoosh_index(app,Day)
    keyword = request.args.get('query')
    results = Day.query.whoosh_search(query,MAX_SEARCH_RESULTS).all()
    print(results)
    return render_template('search_results.html',query=query,results=results)

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())


@app.route('/for_traveler')
def for_traveler():
    return render_template('for_traveler.html',title='for_traveler')
@app.route('/for_guide')
def for_guide():
    return render_template('for_guide.html',title='for_guide')
@app.route('/FAQ_traveler')
def FAQ_traveler():
    return render_template('FAQ_traveler.html',title='FAQ_traveler')
@app.route('/FAQ_guide')
def FAQ_guide():
    return render_template('FAQ_guide.html',title='FAQ_guide')

whooshalchemy.whoosh_index(app, Day)
