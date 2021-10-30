from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    usertype = SelectField('Select Usertype',
                           choices=[('Job Seeker', 'Job Seeker'),
                                    ('Company', 'Company')],
                           validators=[DataRequired()])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken. Please choose a different one.')


class LoginForm(FlaskForm):
    usertype = SelectField('Select Usertype',
                           choices=[('Job Seeker', 'Job Seeker'),
                                    ('Company', 'Company')],
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ReviewForm(FlaskForm):
    username = StringField('Name',
                           validators=[DataRequired()])
    review = TextAreaField('Review',
                           validators=[DataRequired()])
    submit = SubmitField('Submit Review')


class JobForm(FlaskForm):
    title = StringField('Job Title',
                        validators=[DataRequired(), Length(min=2, max=20)])
    industry = SelectField('Industry', choices=[('Construction', 'Construction'),
                                                ('Education', 'Education'),
                                                ('Food And Beverage', 'Food and Beverage'),
                                                ('Pharmaceutical', 'Pharmaceutical'),
                                                ('Entertainment', 'Entertainment'),
                                                ('Manufacturing', 'Manufacturing'),
                                                ('Telecommunication', 'Telecommunication'),
                                                ('Agriculture', 'Agriculture'),
                                                ('Transportation', 'Transportation'),
                                                ('Computer And Technology', 'Computer and Technology'),
                                                ('Healthcare', 'Healthcare'),
                                                ('Media And News', 'Media and News'),
                                                ('Hospitality', 'Hospitality'),
                                                ('Energy', 'Energy'),
                                                ('Fashion', 'Fashion'),
                                                ('Telecommunication', 'Telecommunication'),
                                                ('Finance And Economic', 'Finance and Economic'),
                                                ('Advertising And Marketing', 'Advertising and Marketing'),
                                                ('Mining', 'Mining'),
                                                ('Aerospace', 'Aerospace')],
                           validators=[DataRequired()])
    description = TextAreaField('Job Description',
                                validators=[DataRequired()])
    submit = SubmitField('Submit')


class ApplicationForm(FlaskForm):
    gender = SelectField('Gender', choices=[('Male', 'Male'),
                                            ('Female', 'Female'),
                                            ('Others', 'Other')],
                         default='male',
                         validators=[DataRequired()])
    degree = SelectField('Degree',
                         default='eSchool',
                         choices=[('eSchool', 'School'),
                                  ('dHighSchool', 'HighSchool'),
                                  ('cBachelor', 'Bachelor'),
                                  ('bMaster', 'Master'),
                                  ('aPHD', 'PHD')],
                         validators=[DataRequired()])
    industry = SelectField('Industry',
                           default='Construction',
                           choices=[('Construction', 'Construction'),
                                    ('Education', 'Education'),
                                    ('Food And Beverage', 'Food and Beverage'),
                                    ('Pharmaceutical', 'Pharmaceutical'),
                                    ('Entertainment', 'Entertainment'),
                                    ('Manufacturing', 'Manufacturing'),
                                    ('Telecommunication', 'Telecommunication'),
                                    ('Agriculture', 'Agriculture'),
                                    ('Transportation', 'Transportation'),
                                    ('Computer And Technology', 'Computer and Technology'),
                                    ('Healthcare', 'Healthcare'),
                                    ('Media And News', 'Media and News'),
                                    ('Hospitality', 'Hospitality'),
                                    ('Energy', 'Energy'),
                                    ('Fashion', 'Fashion'),
                                    ('Telecommunication', 'Telecommunication'),
                                    ('Finance and Economic', 'Finance and Economic'),
                                    ('Advertising And Marketing', 'Advertising and Marketing'),
                                    ('Mining', 'Mining'),
                                    ('Aerospace', 'Aerospace')],
                           validators=[DataRequired()])
    experience = IntegerField('Professional Experience in years',
                              validators=[DataRequired()])
    cv = FileField('Update Resume', validators=[FileAllowed(['jpg', 'png', 'bmp'])])
    cover_letter = TextAreaField('Cover Letter',
                                 validators=[DataRequired()])
    submit = SubmitField('Submit')
