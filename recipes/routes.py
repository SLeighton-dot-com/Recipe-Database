from flask import render_template, request, redirect, url_for
from recipes import app, db
from recipes.models import Filter, Recipe


@app.route("/")
def home():
    recipes = list(Recipe.query.order_by(Recipe.id).all())
    return render_template("recipes.html", recipes=recipes)


@app.route("/filters")
def filters():
    filters = list(Filter.query.order_by(Filter.filter_name).all())
    return render_template("filters.html", filters=filters)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    filters = list(Filter.query.order_by(Filter.filter_name).all())
    if request.method == "POST":
        recipe = Recipe(
            recipe_name=request.form.get("recipe_name"),
            recipe_description=request.form.get("recipe_description"),
            main_ingredient=request.form.get("main_ingredient"),
            cooking_method=request.form.get("cooking_method"),
            prep_time=request.form.get("prep_time"),
            recipe_owner=request.form.get("recipe_owner"),
            category_id=request.form.get("category_id")
        )
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_recipe.html", filters=filters)


@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    filters = list(Filter.query.order_by(Filter.filter_name).all())
    if request.method == "POST":
        recipe.recipe_name = request.form.get("recipe_name"),
        recipe.recipe_description = request.form.get("recipe_description"),
        recipe.main_ingredient = request.form.get("main_ingredient"),
        recipe.cooking_method = request.form.get("cooking_method"),
        recipe.prep_time = request.form.get("prep_time"),
        recipe.recipe_owner = request.form.get("recipe_owner"),
        recipe.category_id = request.form.get("category_id")
        db.session.commit()
    return render_template("edit_recipe.html", recipe=recipe, filters=filters)


@app.route("/add_filter", methods=["GET", "POST"])
def add_filter():
    if request.method == "POST":
        filter = Filter(filter_name=request.form.get("filter_name"))
        db.session.add(filter)
        db.session.commit()
        return redirect(url_for("filters"))
    return render_template("add_filter.html")


@app.route("/edit_filter/<int:filter_id>", methods=["GET", "POST"])
def edit_filter(filter_id):
    filter = Filter.query.get_or_404(filter_id)
    if request.method == "POST":
        filter.filter_name = request.form.get("filter_name")
        db.session.commit()
        return redirect(url_for("filters"))
    return render_template("edit_filter.html", filter=filter)


@app.route("/delete_filter/<int:filter_id>")
def delete_filter(filter_id):
    filter = Filter.query.get_or_404(filter_id)
    db.session.delete(filter)
    db.session.commit()
    return redirect(url_for("filters"))


@app.route("/delete_recipe/<int:recipe_id>")
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for("home"))
