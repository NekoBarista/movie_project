from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from form import ReviewForm, AddMovie
import requests

app = Flask(__name__)
app.app_context().push()


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top-movies.db"
app.config['SECRET_KEY'] = 'aadfajdkfakjdf8934795uiajdfkn'
db = SQLAlchemy(app)
Bootstrap(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=False, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String, unique= True, nullable = False)
    rating = db.Column(db.Float, unique=False, nullable=True)
    ranking = db.Column(db.Integer, unique=False, nullable=True)
    review = db.Column(db.String, unique=True, nullable=True)
    img_url= db.Column(db.String, unique=True, nullable=False)

db.create_all()

@app.route('/')
def home():
    all_movies = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars().all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", all_movies = all_movies)

@app.route('/edit', methods=["GET", "POST"])
def edit():
    form = ReviewForm()
    movie_id = request.args.get('id')
    movie = Movie.query.filter_by(id = movie_id).first()
    if form.validate_on_submit():
        movie.rating = form.rating.data
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie = movie, form = form)

@app.route("/delete")
def delete():
    movie_id = request.args.get('id')
    movie = Movie.query.filter_by(id= movie_id).first()
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddMovie()
    if form.validate_on_submit():
        title = form.title.data
        api_key = 'dcc9516c1a9c44f8a0e4438e6a595814'
        result = requests.get(url=f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}")
        data = result.json()
        movie_list = data['results']
        return render_template('select.html', movie_list=movie_list)

    return render_template('add.html', form=form)

@app.route('/find')
def find_movie():
    movie_id = request.args.get('id')
    api_key = 'dcc9516c1a9c44f8a0e4438e6a595814'
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}")
    data = response.json()
    new_movie = Movie(title =data['title'] , year =data["release_date"], description=data['overview'], img_url=f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"  )
    db.session.add(new_movie)
    db.session.commit()
    movie = Movie.query.filter_by(title=data['title']).first()
    return redirect(url_for('edit', id = movie.id))



if __name__ == "__main__":
    app.run(debug=True)
