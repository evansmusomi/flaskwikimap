""" Maps browser requests to Python functions """

from models import db, User
from forms import SignupForm, LoginForm
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

# Connect Flask to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/flaskwikimap'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Configure app to protect against CSRF
app.secret_key = "development-key"


@app.route("/")
def index():
    """ Renders home page """
    return render_template("index.html")


@app.route("/about")
def about():
    """ Renders about page """
    return render_template("about.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    """ Renders the sign up page with form """
    form = SignupForm()

    if request.method == 'POST':
        if form.validate():
            new_user = User(form.first_name.data, form.last_name.data,
                            form.email.data, form.password.data)
            db.session.add(new_user)
            db.session.commit()

            # Create new session
            session['email'] = new_user.email
            return redirect(url_for('home'))

        else:
            return render_template("signup.html", form=form)

    elif request.method == 'GET':
        return render_template("signup.html", form=form)


@app.route("/home")
def home():
    """ Renders the home page """
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Renders the log in page """
    form = LoginForm()

    if request.method == "POST":
        if form.validate():
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session['email'] = form.email.data
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))

        else:
            return render_template("login.html", form=form)

    elif request.method == 'GET':
        return render_template("login.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
