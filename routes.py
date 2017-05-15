""" Maps browser requests to Python functions """

from models import db
from forms import SignupForm
from flask import Flask, render_template

app = Flask(__name__)

# Connects Flask to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/flaskwikimap'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Configures app to protect against CSRF
app.secret_key = "development-key"


@app.route("/")
def index():
    """ Renders home page """
    return render_template("index.html")


@app.route("/about")
def about():
    """ Renders about page """
    return render_template("about.html")


@app.route("/signup")
def signup():
    """ Renders the sign up page with form """
    form = SignupForm()
    return render_template("signup.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
