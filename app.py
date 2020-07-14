import os, logging
from config import Config
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Load configs from config.py
app.config.from_object(Config)

# Create our DB from our app configs we set up
db = SQLAlchemy(app)

# Reusable set up for creating tables in our Database
db.create_all()

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


# Deliver the email to our fake SMTP mailtrap client
def deliver_email(name, email, message):
    port = 587  # Default SMTP port
    smtp_server = "smtp.mailtrap.io"
    login = app.config["MAIL_USERNAME"]
    password = app.config["MAIL_PASSWORD"]
    message = (
        f"<h3>You got mail!</h3> <ul>"
        f"<li>Name: {name}</li>"
        f"<li>Email: {email}</li>"
        f"<li>Message: {message}</li>"
        f"</ul>"
    )
    
    sender_email = email
    receiver_email = "michael.pegios@hotmail.com"
    msg = MIMEText(message, "html")
    msg["Subject"] = f"New Contact Email from {name}"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Send the email
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


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

                # Sends email to Mailtrap
                deliver_email(name, email, message)

                session["alert"] = "success"
                session["details"] = "Thank you for contacting me! I will get back to you shortly."

            return redirect(url_for("index"))

        except Exception as e:
            session["alert"] = "danger"
            session["details"] = "An error has occurred. Please try again."
            print(e)
            f = open("log.txt", "w")
            f.write(f"Exception occurred: {e}")
            f.close()
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
