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
from forms import SignUpForm,LoginForm,Upload
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
  
#----------API ROUTES--------------API ROUTES-----------API ROUTES------------------#

#------------------Authentication Routes----------------------
def jwt_token_required(fn):
    """A decorator functions that secures endpoints that require
    the user to be logged in"""
    @wraps(fn)
    def decorated(*args,**kwargs):
        jwt_token = request.headers.get('Authorization')
        if jwt_token == None:
            return jsonify_errors(['ACCESS DENIED: No token provided'])
        else:
            token_parts = jwt_token.split()
            
            if token_parts[0].lower() != 'bearer':
                return jsonify_errors(['Invalid schema for token'])
            elif len(token_parts) == 1:
                return jsonify_errors(['Token not found'])
            elif len(token_parts)>2:
                return jsonify_errors(['Invalid Token'])
            
            jwt_token = token_parts[1]
            
            try:
                user_data    = jwt.decode(jwt_token,app.config['SECRET_KEY'])
                current_user = User.query.filter_by(username = user_data['user']).first()
            except jwt.exceptions.InvalidSignatureError:
                return jsonify_errors(['ACCESS DENIED: Ivalid Token'])
            except jwt.exceptions.DecodeError:
                return jsonify_errors(['ACCESS DENIED: Ivalid Token'])
            return fn(current_user,*args,**kwargs)
    return decorated


@app.route("/api/auth/login", methods=["POST"])
def login():
    loginForm = LoginForm()
    
    if request.method == "POST" and loginForm.validate_on_submit():
            
        username = loginForm.username.data.lower()
        password = loginForm.password.data
        users    = User.query.filter_by(username=username).all()
        
        if len(users) == 0:
            return jsonify_errors(['Invalid username or password'])
        elif not check_password_hash(users[0].password,password):
            return jsonify_errors(['Invalid username or password'])
        
        else:
            user = users[0]
            jwt_token  = jwt.encode({'user': user.username},app.config['SECRET_KEY'],algorithm = 'HS256')
            response = {'message': 'User successfully logged in','jwt_token':jwt_token,'current_user':user.id}
            return jsonify(response)
    return jsonify_errors(form_errors(loginForm))


@app.route('/api/auth/logout',methods = ['GET'])
@jwt_token_required
def logout(current_user):
    """Logs out a currently logged in user"""
    if request.method == 'GET':
        response = {'message': 'User successfully logged out'}
        return jsonify(response)
    return jsonify_errors(['Only GET requests are accepted'])


#-------------------------Users Reoutes-------------------------

@app.route('/api/users/register', methods = ['POST', 'GET'])
def register():
    signForm = SignUpForm()
    
    if request.method == 'POST' and signForm.validate_on_submit():
        
        users_with_username = User.query.filter_by(username = signForm.username.data).all()
        if len(users_with_username) >0:
            return jsonify_errors(['Username unavailable'])
            
        firstname       = signForm.firstname.data
        lastname        = signForm.lastname.data
        username        = signForm.username.data.lower()
        hashed_password = generate_password_hash(signForm.password.data)
        location        = signForm.location.data
        email           = signForm.email.data
        bio             = signForm.biography.data
        
        photo    = request.files['photo']
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        user = User(username = username, password = hashed_password, firstname = firstname,\
        lastname = lastname, email = email, location = location, biography = bio, \
        profile_photo = filename, joined_on = current_date())
        
        db.session.add(user)
        db.session.commit()
        
        response = {'message': 'User successfully registered'}
        return jsonify(response)
        
        
    return jsonify_errors(form_errors(signForm))
        

@app.route('/api/users/<user_id>',methods = ['GET'])
@jwt_token_required
def get_user_details(current_user,user_id):
    """Returns json object containing the details for the user with
    id <user_id>
    """
    print('here')
    user = User.query.filter_by(id = user_id).first()

    if user == None:
        return jsonify_errors(['User does not exist'])
    
    if request.method == 'GET':
        posts = Post.query.filter_by(userid = user.id)
        number_of_followers = Follow.query.filter_by(userid = user.id).count()
        user_data = dictify(user)
        user_data['joined_on'] = user_data['joined_on'].strftime("%d %B, %Y")
        del user_data['password']
        user_data['number_of_followers'] = number_of_followers
        posts = [post.photo for post in posts]
        return jsonify({'User':user_data,'Posts':posts})
        
    
    
#---------------------------Posts Routes-----------------------------
@app.route('/api/users/<user_id>/posts',methods = ['POST'])
@jwt_token_required
def post(current_user,user_id):
    """Creates post for currently logged in user with id <user_id>"""
    uploadform = Upload()
    user = User.query.filter_by(id = user_id).first()
    
    print(request.files['image'])
    if user == None:
        return jsonify_errors(['User does not exist'])
        
    if request.method == 'POST' and uploadform.validate_on_submit():

        image    = request.files['image']
        caption  = uploadform.caption.data
        print('Image',image)
        print(caption)
        filename = secure_filename(image.filename)
        
        post = Post(userid = user_id,photo = filename,caption = caption,created_on = current_date())
        db.session.add(post)
        db.session.commit()
        image.save('app/static/images/' + filename)
        return jsonify({'message':'Post successfully created'})
    return jsonify_errors(form_errors(uploadform))


@app.route('/api/users/<user_id>/posts',methods = ['GET'])
@jwt_token_required
def view_posts(current_user,user_id):
    """Gets a jsonified list of all the posts made by 
    the user with id <user_id>
    """
    user = User.query.filter_by(id = user_id).first()
    if user == None:
        return jsonify({'error': 'This user does not exist'})
        
    if request.method == 'GET':
        posts         = Post.query.filter_by(userid = user_id).all()
        list_of_posts = [dictify(post) for post in posts]
        for post in list_of_posts:
            post['created_on'] = post['created_on'].strftime('%Y-%m-%d')
            print(post['created_on'])
        return jsonify({'POSTS':list_of_posts})


@app.route('/api/posts',methods = ['GET'])
def get_all_posts():
    """Returns a jsonified list of all posts made by all users"""
    if request.method == 'GET':
        all_posts         = Post.query.all()
        list_of_all_posts = [dictify(post) for post in all_posts]
        
        for post in list_of_all_posts:
            user = User.query.filter_by(id = post['userid']).first()
            post['username'] = user.username
            post['likes'] = Like.query.filter_by(postid = post['id']).count()
            post['created_on'] = post['created_on'].strftime("%d %B, %Y")
            post['user_image'] = user.profile_photo
        return jsonify({'POSTS':list_of_all_posts})
    

#------------------------Follow Routes--------------------------    
@app.route('/api/users/<user_id>/follow',methods = ['POST'])
@jwt_token_required
def follow_user(current_user,user_id):
    """Creates a relationship where the currently logged in 
    user follows the user with id <user_id>
    """
    user = User.query.filter_by(id = user_id).first()
    
    if user == None:
        return jsonify({'error': 'This user does not exist'})
    
    if request.method == 'POST':
        follower_id         = current_user.id
        
        pre_existing_relationship = Follow.query.filter_by(follower_id=follower_id,userid=user_id).first()
        
        if pre_existing_relationship == None:
            follow_relationship = Follow(follower_id=follower_id,userid=user_id)
            print(follow_relationship)
            db.session.add(follow_relationship)
            db.session.commit()
            response = {'message':'You are now following that user','newRelationship':'true'}
            return jsonify(response)
        else:
            response = {'message':'You are already following that user','newRelationship':'false'}
            print(response)
            return jsonify(response)
    

@app.route('/api/users/<user_id>/follow',methods = ['GET'])
@jwt_token_required
def get_number_of_followers(current_user,user_id):
    """Returns a json object with the number of followers for the 
    user with id <user_id>
    """
    user = User.query.filter_by(id = user_id).first()
    
    if user == None:
        return jsonify_errors(['This user does not exist'])
    
    if request.method == 'GET':
        number_of_followers = len(Follow.query.filter_by(userid = user_id).all())
        return jsonify({'followers':number_of_followers})


@app.route('/api/users/<user_id>/following',methods = ['GET'])
@jwt_token_required
def is_following(current_user,user_id):
    """Returns a json object telling whether or not 
    the currently loggd in user is following the user with id
    <user_id>
    """
    user = User.query.filter_by(id = user_id).first()
    
    if user == None:
        return jsonify_errors(['This user does not exist'])
    relationship = Follow.query.filter_by(userid = user_id,follower_id = current_user.id).first()
    
    if relationship == None:
        return jsonify({'following':False})
    else:
        return jsonify({'following':True})
    

#------------------------Likes Routes-------------------------- 
@app.route('/api/posts/<post_id>/like',methods = ['POST'])
@jwt_token_required
def like_post(current_user,post_id):
    """Creates a like relationship where the current users likes 
    the post with id <post_id>
    """
    print('x')
    post    = Post.query.filter_by(id = post_id).first()
    print(post.id)
    user_id = current_user.id
    print(user_id)
    
    if post == None:
        return jsonify_errors(['This post does not exist'])
    
    if request.method == 'POST':
        
        pre_existing_relationship = Like.query.filter_by(postid = post_id,userid = current_user.id).first()
        print(pre_existing_relationship)

        if pre_existing_relationship == None:
            like = Like(postid =post_id,userid = user_id)
            db.session.add(like)
            db.session.commit()
            number_of_likes = len(Like.query.filter_by(postid = post_id).all())
            return jsonify({'message': 'You like that Post','likes':number_of_likes})  
        else:
            number_of_likes = len(Like.query.filter_by(postid = post_id).all())
            return jsonify({'message': 'You already like that Post','likes':number_of_likes})


@app.route('/api/users/<user_id>/like',methods = ['GET'])
@jwt_token_required
def get_liked_posts(current_user,user_id):
    """
    Returns a list of posts liked by the user with user id
    """
    user    = User.query.filter_by(id = user_id).first()
    user_id = current_user.id
    
    if user == None:
        return jsonify_errors(['This user does not exist'])
    
    liked_posts = Like.query.filter_by(userid = user_id).all()
    dict_liked_posts = [dictify(post) for post in liked_posts]
    print(dict_liked_posts)
    return jsonify({'liked_posts':dict_liked_posts})
    
###
# The functions below should be applicable to all Flask apps.
###
def dictify(data_object):
    """
    Returns a dictionary containing the attributes and thier values
    for an object returned from a DB query
    """
    key_value_pairs   = data_object.__dict__.items()
    object_dictionary = {}
    
    for key,value in key_value_pairs:
        if not key == '_sa_instance_state':
        #All db ojects will have this but we do not need it here
        # for example: ('_sa_instance_state', <sqlalchemy.orm.state.InstanceState object at 0x7f6696d831d0>)
            object_dictionary[key] = value
    return object_dictionary


def jsonify_errors(list_of_errors):
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
    response.headers['Cache-Control']   = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
