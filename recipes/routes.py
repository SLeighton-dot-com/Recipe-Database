# Import necessary modules and classes
from flask import render_template, request, redirect, url_for, flash, session
from recipes import app, db
from recipes.models import Filter, Recipe, User
from werkzeug.security import generate_password_hash, check_password_hash


# Define a route for the home page
@app.route("/")
def home():
    # Query and retrieve all recipes from the database, then render them
    # on the 'recipes.html' template
    recipes = list(Recipe.query.order_by(Recipe.id).all())
    return render_template("recipes.html", recipes=recipes)


# Define a route for displaying filters
@app.route("/filters")
def filters():
    # Query and retrieve all filters from the database, then render
    # them on the 'filters.html' template
    filters = list(Filter.query.order_by(Filter.filter_name).all())
    return render_template("filters.html", filters=filters)


# Define a route for user registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Extract username and password from the registration form
        username = request.form.get("username").lower()
        password = request.form.get("password")
        # Check if the username already exists in the 'User' database
        existing_user = User.query.filter_by(username=username).first()
        # If the username already exists, display an error message
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        # Create a new user, set their password, and add them to the database
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        # Log in the new user and redirect to their profile page
        session["user"] = username
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))
    # Render the registration form
    return render_template("register.html")


# Define a route for user login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Extract username and password from the login form
        username = request.form.get("username").lower()
        password = request.form.get("password")
        # Check if the entered username exists and the password is correct
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            # Log in the user and redirect to their profile page
            session["user"] = username
            flash(f"Welcome, {username}")
            return redirect(url_for("profile", username=session["user"]))
        else:
            # Display an error message if login credentials are incorrect
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    # Render the login form
    return render_template("login.html")


# Define a route for user profile
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # Check if the user is authorized to view this profile, if not,
    # redirect to login
    if "user" not in session or session["user"] != username:
        flash("You are not authorized to view this profile.")
        return redirect(url_for("login"))
    # Query and retrieve the user's information from the database and
    # render their profile
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User not found.")
        return redirect(url_for("login"))
    return render_template("profile.html", username=user.username)


# Define a route for user logout
@app.route("/logout")
def logout():
    # Log the user out and redirect to the login page
    flash("You have been logged out")
    session.pop("user", None)
    return redirect(url_for("login"))


# Define a route for adding a new recipe
@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    # Query and retrieve all filters from the database
    filters = list(Filter.query.order_by(Filter.filter_name).all())
    if request.method == "POST":
        # Extract recipe details from the form and add the new recipe to
        # the database
        prep_time_input = request.form.get("prep_time")
        try:
            prep_time_value = int(prep_time_input)
        except ValueError:
            prep_time_value = 0
        recipe_owner = session['user']
        recipe = Recipe(
            recipe_name=request.form.get("recipe_name"),
            recipe_description=request.form.get("recipe_description"),
            main_ingredient=request.form.get("main_ingredient"),
            cooking_method=request.form.get("cooking_method"),
            prep_time=prep_time_value,
            recipe_owner=recipe_owner,
            category_id=request.form.get("filter_id")
        )
        db.session.add(recipe)
        db.session.commit()
        flash("Recipe added successfully!")
        return redirect(url_for("home"))
    # Render the form for adding a new recipe
    return render_template("add_recipe.html", filters=filters)


# Define a route for editing a recipe
@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    # Query and retrieve the recipe to be edited from the database
    recipe = Recipe.query.get_or_404(recipe_id)
    filters = list(Filter.query.order_by(Filter.filter_name).all())
    if request.method == "POST":
        # Extract updated recipe details from the form and update the recipe
        # in the database
        prep_time_input = request.form.get("prep_time")
        try:
            prep_time_value = int(prep_time_input)
        except ValueError:
            prep_time_value = 0
        recipe.recipe_name = request.form.get("recipe_name")
        recipe.recipe_description = request.form.get("recipe_description")
        recipe.main_ingredient = request.form.get("main_ingredient")
        recipe.cooking_method = request.form.get("cooking_method")
        recipe.prep_time = prep_time_value
        filter_id_input = request.form.get("filter_id")
        if filter_id_input:
            recipe.category_id = filter_id_input
        db.session.commit()
        flash("Recipe updated successfully!")
        return redirect(url_for("home"))
    # Render the form for editing the recipe
    return render_template("edit_recipe.html", recipe=recipe, filters=filters)


# Define a route for adding a new filter
@app.route("/add_filter", methods=["GET", "POST"])
def add_filter():
    if request.method == "POST":
        # Extract filter name from the form and add the new filter to
        # the database
        filter = Filter(filter_name=request.form.get("filter_name"))
        db.session.add(filter)
        db.session.commit()
        return redirect(url_for("filters"))
    # Render the form for adding a new filter
    return render_template("add_filter.html")


# Define a route for editing a filter
@app.route("/edit_filter/<int:filter_id>", methods=["GET", "POST"])
def edit_filter(filter_id):
    # Query and retrieve the filter to be edited from the database
    filter = Filter.query.get_or_404(filter_id)
    if request.method == "POST":
        # Extract updated filter name from the form and update the filter
        # in the database
        filter.filter_name = request.form.get("filter_name")
        db.session.commit()
        return redirect(url_for("filters"))
    # Render the form for editing the filter
    return render_template("edit_filter.html", filter=filter)


# Define a route for deleting a filter
@app.route("/delete_filter/<int:filter_id>")
def delete_filter(filter_id):
    # Query and retrieve the filter to be deleted from the database
    # then delete it
    filter = Filter.query.get_or_404(filter_id)
    db.session.delete(filter)
    db.session.commit()
    return redirect(url_for("filters"))


# Define a route for deleting a recipe
@app.route("/delete_recipe/<int:recipe_id>")
def delete_recipe(recipe_id):
    # Query and retrieve the recipe to be deleted from the database
    # then delete it
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for("home"))
