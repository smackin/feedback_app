from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegistrationForm, DeleteForm, LoginForm
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route("/")
def homepage():
    """Homepage of site; redirect to register."""

    return redirect("/register")


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user: produce form and handle form submission."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, email, first_name, last_name)

        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template("users/register.html", form=form)
        
@app.route("/users/<username>")
def show_user(username):

    if 'username' not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.get(username)
    form = DeleteForm()
    
    return render_template('users/show.html', user=user, form=form)
    
    
@app.route('/login', methods=['GET','POST'])
def login():
    """Display login form and handle login"""
    
    if "username" in session: 
            return redirect(f"/users/{session['username']}")
        
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.username.data
        
        user = User.authenticate(username, password)
        if user: 
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["INVALID USERNAME/PASSWORD"]
            return render_template("users/login.html", form=form)
        
    return render_template("users/login.html", form=form)    


@app.route("/logout")
def logout():
    """user log out """
    
    session.pop("username")
    return redirect("/login")