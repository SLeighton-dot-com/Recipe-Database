# Import the database instance and password hashing utility
from recipes import db
from werkzeug.security import generate_password_hash, check_password_hash

# Define a database model for Users
def check_password(self, password):
    return check_password_hash(self.password_hash, password)



# Define a database model for Filters (like categories for recipes)
class Filter(db.Model):
    # Each filter has a unique ID (primary key)
    id = db.Column(db.Integer, primary_key=True)
    # Each filter has a name, which is unique and cannot be empty
    filter_name = db.Column(db.String(40), unique=True, nullable=False)
    # Set up a relationship to the Recipe model
    # (one filter can relate to many recipes)
    recipes = db.relationship("Recipe",
                              backref="filter",
                              cascade="all, delete",
                              lazy=True)

    # Representation method to return the filter's name when printed
    def __repr__(self):
        return self.filter_name


# Define a database model for Users
class User(db.Model):
    # Each user has a unique ID (primary key)
    id = db.Column(db.Integer, primary_key=True)
    # Each user has a unique username, which cannot be empty
    username = db.Column(db.String(50), unique=True, nullable=False)
    # Store the hashed password (not the plain text password)
    password_hash = db.Column(db.String(512))

    # Method to set a user's password, which gets hashed for security
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Representation method to return a user's information when printed
    def __repr__(self):
        return '<User {}>'.format(self.username)


# Define a database model for Recipes
class Recipe(db.Model):
    # Each recipe has a unique ID (primary key)
    id = db.Column(db.Integer, primary_key=True)
    # Each recipe has a unique name, which cannot be empty
    recipe_name = db.Column(db.String(50), unique=True, nullable=False)
    # Description of the recipe, which cannot be empty
    recipe_description = db.Column(db.Text, nullable=False)
    # Main ingredient used in the recipe, which cannot be empty
    main_ingredient = db.Column(db.String(20), nullable=False)
    # Cooking method, which cannot be empty
    cooking_method = db.Column(db.String(15), nullable=False)
    # Preparation time (in minutes), which cannot be empty
    prep_time = db.Column(db.Integer, nullable=False)
    # Owner of the recipe, which cannot be empty
    recipe_owner = db.Column(db.String(30), nullable=False)
    # The category (filter) ID to which the recipe belongs
    # which cannot be empty
    category_id = db.Column(db.Integer, db.ForeignKey(
        "filter.id", ondelete="CASCADE"), nullable=False)

    # Representation method to return a recipe's details when printed
    def __repr__(self):
        return "#{0} - Recipe: {1} | Prep Time: {2}".format(
            self.id, self.recipe_name, self.prep_time
        )
