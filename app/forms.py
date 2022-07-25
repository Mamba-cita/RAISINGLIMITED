from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from flask_ckeditor import CKEditorField



class SearchForm(FlaskForm):
    searched = StringField('Searched', validators=[DataRequired()])
    submit = SubmitField('Submit')
class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(4, 64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(4, 64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(4, 64)])
    confirm_password = StringField('Confirm Password', validators=[DataRequired(), Length(4, 64), EqualTo('password')])
    submit = SubmitField('Register')
    


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')
    
    
    
class PostsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(3, 200)])
    body = CKEditorField('Body', validators=[DataRequired()])
    author = StringField('Author')
    slug = StringField('Slug', validators=[DataRequired(), Length(3, 64)])
    submit = SubmitField('Submit')
    
    