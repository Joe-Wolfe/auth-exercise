from flask import Flask, render_template, redirect, flash, session
from models import db, connect_db, User, Feedback
from forms import loginForm, registerForm, feedbackForm
from sqlalchemy.exc import IntegrityError
import secret

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = secret.SECRET_KEY
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.app_context().push()

connect_db(app)
db.create_all()


@app.route('/')
def goHome():
    """redirect to home page"""
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """register new user"""
    form = registerForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(
            username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username already taken')

            return render_template('register.html', form=form)
        session["username"] = new_user.username
        return redirect('/users/' + new_user.username)
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """login existing user"""
    form = loginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.login(username, password)

        if user:
            session["username"] = user.username
            return redirect('/users/' + user.username)
        else:
            form.username.errors = ['Invalid username/password']
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)


@app.route('/users/<username>')
def showUser(username):
    """secret page for logged in users"""
    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect('/login')
    if session["username"] != username:
        flash("You do not have permission to view!")
        return redirect('/login')

    user = User.query.filter_by(username=username).first()
    return render_template('user.html', user=user)


@app.route('/logout')
def logout():
    """logout user"""
    session.pop('username')
    return redirect('/')


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Delete user."""
    if "username" not in session:
        flash("You are not logged in!")
        return redirect('/login')
    if session["username"] != username:
        flash("You do not have permission to do this!")
        return redirect('/login')

    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    return redirect("/")


@app.route("/feedback/add", methods=["GET", "POST"])
def feedback():
    """feedback page"""
    if "username" not in session:
        flash("You are not logged in!")
        return redirect('/login')
    form = feedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        username = session["username"]
        new_feedback = Feedback(
            title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect("/users/" + username)
    else:
        return render_template("feedback.html", form=form)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """update feedback"""
    if "username" not in session:
        flash("You are not logged in!")
        return redirect('/login')
    feedback = Feedback.query.get_or_404(feedback_id)
    if feedback.username != session["username"]:
        flash("You do not have permission to do this!")
        return redirect('/login')
    form = feedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect("/users/" + feedback.username)
    else:
        return render_template("editFeedback.html", form=form, id=feedback_id)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """delete feedback"""
    if "username" not in session:
        flash("You are not logged in!")
        return redirect('/login')
    feedback = Feedback.query.get_or_404(feedback_id)
    if feedback.username != session["username"]:
        flash("You do not have permission to do this!")
        return redirect('/login')
    db.session.delete(feedback)
    db.session.commit()
    return redirect("/users/" + feedback.username)
