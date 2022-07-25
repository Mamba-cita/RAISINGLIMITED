from unicodedata import name
from click import confirm
from flask import Flask
from sqlalchemy import null
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user,UserMixin




class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Posts', backref='poster')
   
    
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password_hash(self, password):
        return check_password_hash(self.password, password)  

    def __repr__(self):
        return '<User %r>' % self.name
    
    
    
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(200),nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(200),nullable=False)
    #foreign key
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    
    
class Shipments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(80), nullable=False)
    ron = db.Column(db.Integer)
    Shipments_type = db.Column(db.String(80), nullable=False)
    commodity = db.Column(db.String(80), nullable=False)
    total_allocation = db.Column(db.Integer, nullable=False)
    acc_manager = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now())

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transport_rate = db.Column(db.Integer, nullable=False)
    truck_reg =db.Column(db.String(80), nullable=False)
    qty_to_load = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.String(80))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now()) 
  
    
    
    
    #db.create_all()