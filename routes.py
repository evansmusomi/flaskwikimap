""" Maps browser requests to Python functions """

from models import db
from flask import Flask, render_template

app = Flask(__name__)

# Connects Flask to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/flaskwikimap'
db.init_app(app)


@app.route("/")
def index():
    """ Renders home page """
    return render_template("index.html")


@app.route("/about")
def about():
    """ Renders about page """
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
