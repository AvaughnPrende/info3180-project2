"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os, datetime
from app import app,db
from flask import render_template, request, redirect, url_for, flash, jsonify,session,abort
from flask_login import login_user, logout_user, current_user, login_required
from app import models
from forms import SignUpForm,LoginForm
from werkzeug.utils import secure_filename
from app.models import User,Post, Follow, Like
from werkzeug.security import generate_password_hash, check_password_hash
from auxiliary_functions import current_date
import jwt
from functools import wraps

###
# Routing for your application.
###

@app.route('/')
def index():
    """Render the initial webpage and then let VueJS take control."""
    return render_template('index.html')
  

@app.route('/register', methods = ['POST', 'GET'])
def register():
    
    signForm = SignUpForm()
    
    if request.method == 'POST' and signForm.validate_on_submit():
        firstname       = signForm.firstname.data
        lastname        = signForm.lastname.data
        username        = signForm.username.data
        hashed_password = generate_password_hash(signForm.password.data)
        location        = signForm.location.data
        email           = signForm.email.data
        bio             = signForm.bio.data
        
        photo    = request.files['image']
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        #userId = createId(first,last,gender)
        
        user = User(username = username, password = hashed_password, firstname = firstname,\
        lastname = lastname, email = email, location = location, biography = bio, \
        profile_photo = filename, joined_on = current_date())
        
        db.session.add(user)
        db.session.commit()
        
        response = {'message': 'User successfully registered'}
        return jsonify(response)
        
    else:
        return jsonify_form_errors(form_errors(signForm))
        


@app.route("/login", methods=["GET", "POST"])
def login():
    loginForm = LoginForm()
    
    if request.method == "POST" and loginForm.validate_on_submit():
            
        username = loginForm.username.data
        password = loginForm.password.data
        
        users  = User.query.filter_by(username=username).all()
        
        if len(users) == 0:
            return jsonify({'error': 'Invalid username or password'})
        elif not check_password_hash(users[0].password,password):
            return jsonify({'error': 'Invalid username or password'})
        else:
            user = users[0]
            jwt_token  = jwt.encode({'user': user.username},app.config['SECRET_KEY'],algorithm = 'HS256')
            response = {'message': 'User successfully logged in','jwt_token':jwt_token}
            return jsonify(response)
    else:
        return jsonify_form_errors(form_errors(loginForm))


def jwt_token_required(fn):
    """A decorator functions that secures endpoints that require
    the user to be logged in"""
    @wraps(fn)
    def decorated(*args,**kwargs):
        jwt_token = request.headers.get('Authorization')
        if jwt_token == None:
            return jsonify({'error':'ACCESS DENIED: No token provided'})
        else:
            try:
                user_data    = jwt.decode(jwt_token,app.config['SECRET_KEY'])
                current_user = User.query.filter_by(username = user_data['user']).first()
            except jwt.exceptions.InvalidSignatureError:
                return jsonify({'error':'ACCESS DENIED: Ivalid Token'})
            return fn(current_user,*args,**kwargs)
    return decorated


#log in required
@app.route('/logout',methods = ['GET'])
@jwt_token_required
def logout(current_user):
    """Logs out a currently logged in user"""
    if request.method == 'GET':
        return jsonify({'message':current_user.username +  ' successfully logged out'})


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash("You are now logged out","danger")
#     """Render the website's about page."""
#     return redirect(url_for("index"))


# @app.route('/explore')
# @login_required
# def explore():
#     users = User.query.all()
#     return render_template('explore.html', users=users)

@app.route('/users/{user_id}')
def userProfile(user_id):
    """Render the website's about page."""
    user = User.query.get(user_id)
    post = Post.query.get(user_id)
    
    posts         = Post.query.filter_by(user_id=User.user_id)
    count_post    = posts.count()
    follows       = Follow.query.filter_by(user_id = Follow.user_id)
    count_follows = follows.count()
    
    return render_template('userProfile.html', user=user, count_post = count_post, count_follows = count_follows, post = post)

@app.route('/posts/new')
def post():
    """Render the website's about page."""
    return render_template('post.html')

###
# The functions below should be applicable to all Flask apps.
###

def jsonify_form_errors(list_of_errors):
    """Returns a json object containing the errors from the form"""
    errors_list = []
    for error in list_of_errors:
        errors_list.append(dict({'error':error}))
    return jsonify({'Errors':errors_list})


def form_errors(form):
    """Collects form errors from a Flask-WTF validation"""
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages


def createId(firstname,password,username):
    fname = firstname[:4]
    Pass = password[:2]
    uname = username[:4]
    id = fname+Pass.upper()+uname
    return id
    

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
