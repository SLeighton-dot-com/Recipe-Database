from flask import render_template, request, redirect, url_for
from recipes import app, db
from recipes.models import Filter, Recipe


@app.route("/")
def home():
    return render_template("recipes.html")


@app.route("/filters")
def filters():
    filters = list(Filter.query.order_by(Filter.filter_name).all())
    return render_template("filters.html", filters=filters)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    filters = list(Filter.query.order_by(Filter.filter_name).all())
    if request.method == "POST":
        filter = Filter(
            recipe_name=request.form.get("recipe_name"),
            recipe_description=request.form.get("recipe_description"),
            main_ingredient=request.form.get("main_ingredient"),
            cooking_method=request.form.get("cooking_method"),
            prep_time=request.form.get("prep_time"),
            recipe_owner=request.form.get("recipe_owner")
        )
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_recipe.html")


@app.route("/add_filter", methods=["GET", "POST"])
def add_filter():
    if request.method == "POST":
        filter = Filter(filter_name=request.form.get("filter_name"))
        db.session.add(filter)
        db.session.commit()
        return redirect(url_for("filters"))
    return render_template("add_filter.html")