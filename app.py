from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    words = ["Metsä", "Kukkulat", "Leiri"]
    return render_template("index.html", message="Pelialueet:", items=words)