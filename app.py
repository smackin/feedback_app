from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegistrationForm, DeleteForm, LoginForm, FeedbackForm
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


@app.route("/users/<username>/delete", methods=['POST'])
def delete_user(username):
    
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    db.session.pop("username")
    
    return redirect("/login")

@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def new_feedback(username):
    """Show add-feedback form and process it."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = FeedbackForm(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("feedback/new.html", form=form)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show update-feedback form and process it."""

    feedback = FeedbackForm.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("/feedback/edit.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = FeedbackForm.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")