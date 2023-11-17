import os
from recipes import app


if __name__ == "__main__":

    def create_tables(self):
        with app.app_context():
            db.create_all()
    create_tables(db)
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=os.environ.get("DEBUG")
    )
    