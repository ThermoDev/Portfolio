from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        print("POST!")


if __name__ == "__main__":
    #app.debug = True
    app.run()
