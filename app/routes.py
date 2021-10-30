from flask import render_template, url_for, flash, redirect, request, send_file
from app import app, db, bcrypt
from PIL import Image
import os
import secrets
from app.forms import RegistrationForm, LoginForm, ReviewForm, JobForm, ApplicationForm
from app.models import User, Jobs, Review, Application
from flask_login import login_user, current_user, logout_user, login_required
import random

rev = [
    {
        'username': 'Micheal Scott',
        'review': 'I hired multiple people using this website. Thank you'
    },
    {
        'username': 'Dwight Schrute',
        'review': 'It could be better'
    },
    {
        'username': 'Andy Bernard',
        'review': 'Best website ever'
    }
]


Review_Obj = Review.query.all()
if len(Review_Obj) < 3:
    Random_Review = rev
else:
    Random_Review = random.sample(Review_Obj, 3)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if current_user.usertype == 'Job Seeker':
            return redirect(url_for('show_jobs'))
        elif current_user.usertype == 'Company':
            return redirect(url_for('posted_jobs'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, usertype=form.usertype.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('You account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, Random_Review=Random_Review)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.usertype == 'Job Seeker':
            return redirect(url_for('show_jobs'))
        elif current_user.usertype == 'Company':
            return redirect(url_for('posted_jobs'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print('password clear')
            if form.usertype.data == user.usertype and form.usertype.data == 'Company':
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('posted_jobs'))
            elif form.usertype.data == user.usertype and form.usertype.data == 'Job Seeker':
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('show_jobs'))
            else:
                flash('Login Unsuccessful. Please check email, password and usertype', 'danger')
        else:
            flash('Login Unsuccessful. Please check email, password and usertype', 'danger')
            return render_template('login.html', form=form, Random_Review=Random_Review)
    return render_template('login.html', form=form, Random_Review=Random_Review)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('show_jobs'))

def save_picture(form_picture):
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f_name + f_ext
    picture_path = os.path.join(app.root_path, 'static', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route("/post_cvs/<jobid>", methods=['GET', 'POST'])
@login_required
def post_cvs(jobid):
    form = ApplicationForm()
    job = Jobs.query.filter_by(id=jobid).first()
    if form.validate_on_submit():
        application = Application(gender=form.gender.data,
                              degree=form.degree.data,
                              industry=form.industry.data,
                              experience=form.experience.data,
                              cover_letter=form.cover_letter.data,
                              application_submiter=current_user,
                              application_jober=job,
                              cv=form.cv.data.filename)
        print(form.cv.data)
        picture_file = save_picture(form.cv.data)
        db.session.add(application)
        db.session.commit()
        return redirect(url_for('show_jobs'))
    return render_template('post_cvs.html', form=form, Random_Review=Random_Review)

@app.route("/post_jobs", methods=['GET', 'POST'])
@login_required
def post_jobs():
    form = JobForm()
    if form.validate_on_submit():
        job = Jobs(title=form.title.data,
                   industry=form.industry.data,
                   description=form.description.data,
                   job_applier=current_user)
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('posted_jobs'))
    return render_template('post_jobs.html', form=form, Random_Review=Random_Review)


@app.route("/review", methods=['GET', 'POST'])
@login_required
def review():
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(username=form.username.data,
                            review=form.review.data)
        db.session.add(review)
        db.session.commit()
        flash('Thank you for providing the review!', 'success')
        return redirect(url_for('show_jobs'))
    return  render_template('review.html', form=form, Random_Review=Random_Review)

@app.route("/posted_jobs")
@login_required
def posted_jobs():
    jobs = Jobs.query.filter_by(job_applier=current_user)
    return render_template('show_jobs.html', jobs=jobs, Random_Review=Random_Review)


@app.route("/show_applications/<jobid>", methods=['GET'])
@login_required
def show_applications(jobid):
    applications = Application.query.filter_by(job_id=jobid).order_by(Application.degree, Application.experience.desc()).all()
    return render_template('show_applications.html', applications=applications, Random_Review=Random_Review)

@app.route("/meeting/<application_id>")
@login_required
def meeting(application_id):
    applicant_id = Application.query.get(int(application_id)).user_id
    applicant = User.query.get(applicant_id)
    return render_template('meeting.html', applicant=applicant, Random_Review=Random_Review)

@app.route("/")
@app.route("/show_jobs")
def show_jobs():
    jobs = Jobs.query.all()
    return render_template('show_jobs.html', jobs=jobs, Random_Review=Random_Review)

@app.route("/resume/<id>", methods=['GET'])
def resume(id):
    cv = Application.query.get(int(id)).cv
    return render_template('resume.html', cv=cv, Random_Review=Random_Review, id=id)

