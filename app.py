from flask import Flask, render_template, request, redirect, url_for, flash, jsonify













#initialize the app
app = Flask(__name__ )







#routes


#our index route will act as our web page
#index route

@app.route('/')
def index():
    return render_template('web_index/templates/index.html')





#protected routes

#home route

@app.route('/home')
def home():
    return 'Hello World, home page'








































#app runs on localhost:5000

if __name__ == '__main__':
    app.run(debug=True)