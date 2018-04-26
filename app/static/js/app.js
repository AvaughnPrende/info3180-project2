/* Add your Application JavaScript */
Vue.component('app-header', {
    template: `
        <header>
            <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
              <a class="navbar-brand" href="#"><img src="/static/images/logo.png" height="48px" width="120px" alt="Logo"></a>
              <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav mr-auto">
                <li class="nav-item active">
                    <router-link class="nav-link" to="/">Home<span class="sr-only">(current)</span></router-link>
                </li>
                <li class="nav-item active">
                    <router-link class="nav-link" to="/loginform">Login<span class="sr-only">(current)</span></router-link>
                </li>
                <li class="nav-item active">
                    <router-link class="nav-link" to="/register">Sign Up<span class="sr-only">(current)</span></router-link>
                </li>
                </ul>
              </div>
            </nav>
        </header>    
    `
});


const Home = Vue.component('home', {
    template: `
    <div class="containment-box">
        <div class="logo">
            <div>
                <!--App LOGO-->
                <img src="/static/images/logo.png" height="220px" width="550px" alt="Logo">
            </div>
        </div>
        <div class="phrase">
            <!--App Tagline/Catch Phrase-->
            <p>{{ welcome }}</p>
        </div>
    </div>   
    `,
    data: function() {
            return {
                welcome: 'Let the World See the Best You.'
            };
        }
});



Vue.component('app-footer', {
    template: `
        <footer>
            <div class="container">
                <p>Copyright &copy {{ year }} PhotoGram Inc.</p>
            </div>
        </footer>
    `,
    data: function() {
        return {
            year: (new Date).getFullYear()
        };
    }
});



const loginForm = Vue.component('loginform',{
    template:
    `
    <div class="fcont">
        <div class="login-form">
            <div class="head">
            <h2>Please Log in</h2>
            </div>
            <br>
            {{token}}
            <div class="form-ish">
                <form action="" method="post" name = 'login_form' id = 'loginform'>
                <div class="form-group">
                    <label   for = 'username'     id = 'username_label'><h5>Username:</h5></label>
                    <input class = 'form-control' id = 'username' type = 'text' name = 'username' rows = '5' placeholder="Enter Username" >
                </div>
                
                <div class="form-group">
                    <label   for = 'password'     id = 'password_label'><h5>Password:</h5></label>
                    <input class = 'form-control' id = 'password' type = 'password' name = 'password' placeholder="Enter Password">
                </div>
                <div class="form-group">
                    <button type="submit" name="submit" class="btn btn-primary">Log in</button>
                </div>
                </form>
            </div>
        </div>
    </div>
    `,
    data:function (){
        return {
            token: token
        };
    }
    
});

const signupForm = Vue.component('signupform',{
    template:
    `
    <div class="scont">
        <div id = 'register-page'>
            <div class="head">
                <h2>Register</h2>
            </div>
            <form action="" method="post" name = 'signup_form' id = 'signupform' enctype = 'multipart/form-data'>
                <div class="form-group">
                    <label   for = 'username' id = 'username_label'> <h5>Username</h5> </label>
                    <input class = 'form-control' id = 'username' type = 'text' name = 'username' rows = '5' placeholder="Enter Username">
                </div>
                
                <div class="form-group">
                    <label   for = 'password' id = 'password_label'> <h5>Password</h5> </label>
                    <input class = 'form-control' id = 'password' type = 'password' name = 'password' rows = '5' placeholder="Enter Password">
                </div>
                
                <div class="form-group">
                    <label   for = 'firstname' id = 'firstname_label'> <h5>Firstname</h5> </label>
                    <input class = 'form-control' id = 'firstname' type = 'text' name = 'firstname' rows = '5' placeholder="Firstname">
                </div>
                
                <div class="form-group">
                    <label   for = 'lastname' id = 'lastname_label'> <h5>Lastname</h5> </label>
                    <input class = 'form-control' id = 'lastname' type = 'text' name = 'lastname' rows = '5' placeholder="Lastname">
                </div>
                
                <div class="form-group">
                    <label   for = 'email' id = 'email_label'> <h5>Email</h5> </label>
                    <input class = 'form-control' id = 'email' type = 'text' name = 'email' rows = '5' placeholder="eg. yourname@example.com">
                </div>
                
                <div class="form-group">
                    <label   for = 'location' id = 'location_label'> <h5>Location</h5> </label>
                    <input class = 'form-control' id = 'location' type = 'text' name = 'location' rows = '5' placeholder="eg. Ibiza, Spain">
                </div>
                
                <div class="form-group">
                    <label   for = 'biography' id = 'biography_label'> <h5>Biography</h5> </label>
                    <textarea class = 'form-control' id = 'biography' name = 'biography' rows = '5'></textarea>
                </div>
            
                <div class="form-group">
                    <label   for = 'photo' id = 'photo_label'> <h5>Photo</h5> </label>
                    <input id = 'photo' type = 'file' name = 'photo'>
                </div><br>
                
                <div class="form-group">
                    <button type="submit" name="submit" class="btn btn-primary">Sign Up</button>
                </div>
            </form>
        </div>
    </div>
    `
});

const profile = Vue.component('profile',{
    template:
    `
    <div class="outside">
        <div class="top">
            <div class="top-right">
                <div class="propic">
                    <img src="{{url_for('static', filename = "images/"+ user.profile_photo) }}"></img>
                </div>
                <div class="userdeets">
                    <div class="uname">
                        <h3>{{ user.username }}</h3>
                    </div>
                    <div class="uflname">
                        <h5>{{ user.firstname }} { {user.lastname }}</h5>
                    </div>
                    <div class="locndate">
                        <p>{{ user.location }} <br> {{user.joined_on }}</p>
                    </div>
                    <div class="bio">
                        <p>{{ user.biogrphy }}</p>
                    </div>
                </div>
            </div>
        
            <div class="top-left">
                <div class="count">
                    <div class="posts">
                        <h5>{{ count_post }}</h5>
                        <h6>Posts</h6>
                    </div>
                    <div class="folrs">
                        <h5>{{ count_follows }}</h5> <!-- ignore for now {{ counter }} -->
                        <h6>Followers</h6>
                    </div>
                    <div class="folwg">
                        <h5>{{ count_following }}</h5>
                        <h6>Following</h6>
                    </div>
                </div>
                <div class="btn">
                    <button type="button" class="btn btn-primary" v-on:click="counter += 1>Follow</button>
                </div>
            </div>
        </div>
        
        <div class="bttm">
            <div class="imgupld">
                {% for images in images %}
                <div class="col-lg-3 col-md-4 col-xs-6 thumb">
                    <img class="img-responsive" src=" {{url_for('static', filename= 'images/' + user.photo)}}" height="275" width="275" alt = "image upload" >
                </div>
                {% endfor %}
            <div>
        </div>
    </div>
    `,
    data:function (){
        return {
            token: token
        };
    }
    
});

// Define Routes
const router = new VueRouter({
    routes: [
        { path: "/",           component: Home },
        { path: "/loginform",  component: loginForm},
        { path: "/register",   component: signupForm}
    ]
});


//Intantioation of the new Vue App
let app = new Vue({
    el: '#app',
    data: {
        welcome: 'Let the World See the Best You.'
    },router
});