from . import db

class Post(db.Model):
    """This is the schema to be used to create the 'posts' table for the 
        photogram database
    """
    __tablename__ = 'posts'
    
    id         = db.Column(db.Integer,primary_key = True)
    userid     = db.Column(db.Integer)
    photo      = db.Column(db.Text)
    caption    = db.Column(db.Text)
    created_on = db.Column(db.Date)
    
    def __init__(self,userid,photo,caption,created_on ):
        """This is the constructor for the Post class"""
        self.userid     = userid
        self.photo      = photo
        self.caption    = caption
        self.created_on = created_on
        
    def __repr__(self):
        return "<Post Made by user {0} - created on {1}>".format(self.userid,self.created_on)


class User(db.Model):
    """This is the schema to be used to create the 'users' table for the 
        photogram database
    """
    __tablename__ = 'users'
    
    id            = db.Column(db.Integer,primary_key = True)
    username      = db.Column(db.String(255))
    password      = db.Column(db.Text)
    firstname     = db.Column(db.String(255))
    lastname      = db.Column(db.String(255))
    email         = db.Column(db.String(255))
    location      = db.Column(db.String(255))
    biography     = db.Column(db.Text)
    profile_photo = db.Column(db.String(255))
    joined_on     = db.Column(db.Date)
    
    def __init__(self,username,password,firstname,lastname,email,location,biography,profile_photo,joined_on):
        """This is the constructor for the User class"""
        self.username      = username
        self.password      = password
        self.firstname     = firstname
        self.lastname      = lastname
        self.email         = email
        self.location      = location
        self.biography     = biography
        self.profile_photo = profile_photo
        self.joined_on     = joined_on
    
    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support
        
    def __repr__(self):
        return '<User {0}: {1} {2}>'.format(self.username,self.firstname,self.lastname)


class Like(db.Model):
    """This is the schema to be used to create the 'likes' table for the 
        photogram database
    """
    __tablename__ = 'likes'
    
    id     = db.Column(db.Integer,primary_key = True) 
    userid = db.Column(db.Integer)
    postid = db.Column(db.Integer)
    
    def __init__(self,userid,postid):
        """This is the constructor for the User class"""
        self.userid = userid
        self.postid = postid

    
    def __repr__(self):
        return '<Like User: {0} - Post: {1}>'.format(self.userid,self.postid)
        

class Follow(db.Model):
    """This is the schema to be used to create the 'follows' table for the 
        photogram database
    """
    __tablename__ = 'follows'
    
    id = db.Column(db.Integer,primary_key = True)
    userid      =db.Column(db.Integer)
    follower_id = db.Column(db.Integer)
    
    def __init__(self,userid,follower_id):
        """This is the constructor for the Follow class"""
        self.userid      = userid
        self.follower_id = follower_id
        
    def __repr__(self):
        return '<Follow User: {0} - Followed by: {1}>'.format(self.userid,self.follower_id)