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
        <div>
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
                <p>Copyright &copy {{ year }} Flask Inc.</p>
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
        <div class="login-form">
        <h2>Please Log in</h2>
        <br>
        {{token}}
        <form action="" method="post" name = 'login_form' id = 'loginform'>
          <div class="form-group">
            <label   for = 'username'     id = 'username_label'><h5>Username</h5></label>
            <input class = 'form-control col-md-6' id = 'username' type = 'text' name = 'username' rows = '5'>
          </div>
          <div class="form-group">
            <label   for = 'password'     id = 'password_label'><h5>Password</h5></label>
            <input class = 'form-control col-md-6' id = 'password' type = 'password' name = 'password'>
          </div>
          <button type="submit" name="submit" class="btn btn-primary btn-block col-sm-1">Log in</button>
        </form>
      </div>
    `,
    data:function (){
        return {
            token: token
        }
    }
    
})

const signupForm = Vue.component('signupform',{
    template:
    `
    
    `
})


// Define Routes
const router = new VueRouter({
    routes: [
        { path: "/",           component: Home },
        { path: "/loginform",  component: loginForm}
    ]
});


//Intantioation of the new Vue App
let app = new Vue({
    el: '#app',
    data: {
        welcome: 'Let the World See the Best You.'
    },router
});