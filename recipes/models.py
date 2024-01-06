from recipes import db
from werkzeug.security import generate_password_hash


class Filter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filter_name = db.Column(db.String(40), unique=True, nullable=False)
    recipes = db.relationship("Recipe",
                              backref="filter",
                              cascade="all, delete",
                              lazy=True)

    def __repr__(self):
        return self.filter_name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(512))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(50), unique=True, nullable=False)
    recipe_description = db.Column(db.Text, nullable=False)
    main_ingredient = db.Column(db.String(20), nullable=False)
    cooking_method = db.Column(db.String(15), nullable=False)
    prep_time = db.Column(db.Integer, nullable=False)
    recipe_owner = db.Column(db.String(30), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        "filter.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return "#{0} - Recipe: {1} | Prep Time: {2}".format(
            self.id, self.recipe_name, self.prep_time
        )


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(25), unique=True, nullable=False)
    user_password = db.Column(db.String(30), unique=True, nullable=False)
    user_email = db.Column(db.String(75), unique=True, nullable=True)
