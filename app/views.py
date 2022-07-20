from app import app,forms,models
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify






#decorator to use for every view


#website home page

@app.route('/')
def index():
    return render_template('web_index/templates/index.html')


















