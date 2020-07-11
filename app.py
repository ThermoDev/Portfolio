import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy


# Our base directory where our DB will be stored
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = "SECRET_KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create our DB from our app configs we set up
db = SQLAlchemy(app)

# Class for our Contact inheriting from our Model to set up a table in our db
class Contact(db.Model):
    # Custom Table Name
    __tablename__ = "contacts"

    # Columns in our DB
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(320), nullable=False)
    message = db.Column(db.Text, nullable=False)

    # Constructor
    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message

    # String representation of the Contact
    def __repr__(self):
        new_line = "\n"
        return f"Contact {self.name} with email {self.email} has sent a Message: {self.message} {new_line}"

# Reusable set up for creating tables in our Database
db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    alert = ""
    details = ""
    # Sets variables a current session, then clears them
    if "alert" in session and "details" in session:
        alert = session["alert"]
        details = session["details"]
        session["alert"] = None
        session["details"] = None

    # Handle POST request
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            message = request.form["message"]

            if name == "" or email == "" or message == "":
                session["alert"] = "dark"
                session["details"] = "Missing entries in the contact form. Could not submit."
            else:
                print(name, email, message)
                # Add data to DB
                db.session.add(Contact(name, email, message))
                # Commit to DB
                db.session.commit()
                session["alert"] = "success"
                session["details"] = "Thank you for contacting me!"

            return redirect(url_for("index"))

        except Exception as e:
            session["alert"] = "danger"
            session["details"] = "An error has occurred. Please try again."
            print(e)
            return redirect(url_for("index"))

    return render_template("index.html", alert=alert, details=details)


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/react")
def react():
    return render_template("react.html")


if __name__ == "__main__":
    app.run()
