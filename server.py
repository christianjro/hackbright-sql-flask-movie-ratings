"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route("/")
def homepage():
    """View homepage."""
    return render_template("homepage.html")


@app.route("/movies")
def all_movies():
    """View all movies."""
    movies = crud.get_all_movies()
    return render_template("all_movies.html", movies=movies)


@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """Show details on a particular movie."""

    movie = crud.get_movie_by_id(movie_id)
    return render_template("movie_details.html", movie=movie)


@app.route("/users")
def all_users():
    """View all users."""
    users = crud.get_all_users()
    return render_template("all_users.html", users=users)


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""
    user = crud.get_user_by_id(user_id)
    user_ratings = crud.get_ratings_by_user(user)
    return render_template("user_details.html", user=user, user_ratings=user_ratings)

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""
    email = request.form.get("email")
    password = request.form.get("password")

    is_user_in_db = crud.get_user_by_email(email)

    if is_user_in_db:
        flash("Account already exists. Please log in.")
    else:
        flash("Account created! Please log in.")
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    connect_to_db(app)

    app.run(host="0.0.0.0", debug=True)
