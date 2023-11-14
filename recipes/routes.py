from flask import render_template
from recipes import app, db
from recipes.models import Filter, Recipe


@app.route("/")
def home():
    return render_template("recipes.html")


@app.route("/filters")
def filters():
    return render_template("filters.html")