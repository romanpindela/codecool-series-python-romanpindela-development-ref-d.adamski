import ast

from flask import Flask, render_template, url_for, jsonify, redirect, request, session
from flask_bcrypt import Bcrypt
from data import queries
import math
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
app = Flask('codecool_series')
app.secret_key = "supersecret"
bcrypt = Bcrypt(app)
SHOWS_PER_PAGE = 15
SHOWN_PAGE_NUMBERS = 5  # should be odd to have a symmetry in pagination


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/shows/')
@app.route('/shows/<int:page_number>')
@app.route('/shows/most-rated/')
@app.route('/shows/most-rated/<int:page_number>')
@app.route('/shows/order-by-<order_by>/')
@app.route('/shows/order-by-<order_by>-<order>/')
@app.route('/shows/order-by-<order_by>/<int:page_number>')
@app.route('/shows/order-by-<order_by>-<order>/<int:page_number>')
def shows(page_number=1, order_by="rating", order="DESC"):
    count = queries.get_show_count()
    pages_count = math.ceil(count[0]['count'] / SHOWS_PER_PAGE)
    shows = queries.get_shows_limited(order_by, order, SHOWS_PER_PAGE, (page_number - 1) * SHOWS_PER_PAGE)

    shown_pages_start = int(page_number - ((SHOWN_PAGE_NUMBERS - 1) / 2))
    shown_pages_end = int(page_number + ((SHOWN_PAGE_NUMBERS - 1) / 2))
    if shown_pages_start < 1:
        shown_pages_start = 1
        shown_pages_end = SHOWN_PAGE_NUMBERS
    elif shown_pages_end > pages_count:
        shown_pages_start = pages_count - SHOWN_PAGE_NUMBERS + 1
        shown_pages_end = pages_count

    return render_template(
        'shows.html',
        shows=shows,
        pages_count=pages_count,
        page_number=page_number,
        shown_pages_start=shown_pages_start,
        shown_pages_end=shown_pages_end,
        order_by=order_by,
        order=order
    )


@app.route('/show/<int:id>/')
def show(id):
    show = queries.get_show(id)
    characters = queries.get_show_characters(id)
    seasons = queries.get_show_seasons(id)

    # format character names
    show['characters_str'] = \
        ', '.join([character['name'] for character in characters])

    # getting trailer id from URL to embed video
    show['trailer_id'] = \
        show['trailer'][show['trailer'].find('=') + 1:] if show['trailer'] else ''

    # format runtime
    hours, minutes = divmod(show['runtime'], 60)
    runtime_str = (str(hours) + 'h ' if hours else '') + (str(minutes) + 'min' if minutes else '')
    show['runtime_str'] = runtime_str

    return render_template('show.html', show=show, seasons=seasons)


@app.route("/show/<int:show_id>/<int:season_id>")
def season(show_id, season_id):
    show = queries.get_show(show_id)
    season = queries.get_season(season_id)[0]
    episodes = queries.get_episodes(season_id)
    return render_template("season.html", show=show, episodes=episodes, season=season)


@app.route("/shows/<phrase>")
def find_show(phrase):
    return jsonify(queries.get_shows_like(str(phrase)))


@app.route("/register", methods=["POST"])
def create_user():
    data = ast.literal_eval(request.data.decode("utf-8"))
    hashed_password = bcrypt.generate_password_hash(data.get('password')).decode("utf-8")
    queries.create_user(data.get('username'), hashed_password)
    return jsonify(userCreated=True)


@app.route("/user/<username>")
def get_user(username):
    user = queries.get_username(username)
    if user:
        return jsonify(user)
    else:
        return jsonify("")


@app.route("/login", methods=["POST"])
def login():
    data = ast.literal_eval(request.data.decode("utf-8"))
    user = queries.get_user(data.get("username"))[0]
    user_password = user.get("password")
    if "username" not in session and bcrypt.check_password_hash(user_password, data.get("password")):
        session["logged"] = True
        session["username"] = data.get("username")
        return jsonify(logged=True)
    else:
        return jsonify(logged=False)


@app.route("/logout", methods=["POST"])
def logout():
    if "logged" in session:
        session.clear()
        return jsonify(loggedOut=True)
    else:
        return jsonify(loggedOut=False)


@app.route("/edit", methods=["GET", "POST"])
def edit_show():
    if "username" in session:
        found_shows = queries.get_all_shows_info()
        return render_template("edit.html", shows=found_shows)
    else:
        return redirect(url_for("index"))


@app.route("/get_seasons/<id>")
def get_show_by_id(id):
    found_seasons = queries.get_show_seasons(id)
    if found_seasons:
        for season in found_seasons:
            season['rating'] = float(season['rating'])
        return jsonify(found_seasons)
    else:
        return jsonify("NO FOUND")


@app.route("/get_episodes/<season_id>")
def get_episodes(season_id):
    episodes = queries.get_episodes(season_id)
    if episodes:
        return jsonify(episodes)
    else:
        return jsonify("NO FOUND")


@app.route("/get_episode/<episode_id>")
def get_episode(episode_id):
    episode = queries.get_episode_details(episode_id)
    if episode:
        return jsonify(episode)
    else:
        return jsonify("NOT FOUND")


@app.route("/update_episode", methods=["POST"])
def update_episode():
    try:
        data = ast.literal_eval(request.data.decode("utf-8"))
        queries.update_episode(data.get("episode_id"), data.get("title"), data.get("overview"))
        return jsonify(updated=True)
    except:
        return jsonify(updated=False)


@app.route("/add_episode", methods=["POST"])
def add_episode():
    try:
        data = ast.literal_eval(request.data.decode("utf-8"))
        queries.add_episode(
            season_id=data.get("season_id"),
            episode_number=data.get("episode_number"),
            title=data.get("title"),
            overview=data.get("overview")
        )
        return jsonify(added=True)
    except:
        return jsonify(added=False)


@app.route("/show/<int:show_id>/<int:season_id>/<int:episode_id>")
def show_episode(show_id, season_id, episode_id):
    show = queries.get_show(show_id)
    season = queries.get_season(season_id)[0]
    episode = queries.get_episode_details(episode_id)

    return render_template("episode.html", show=show, season=season, episode=episode)


@app.route("/add_new_season", methods=["POST"])
def add_season():
    try:
        data = ast.literal_eval(request.data.decode("utf-8"))
        queries.add_season(
            season_number=data.get("season_number"),
            show_id=data.get("show_id"),
            title=data.get("title"),
            overview=data.get("overview")
        )
        return jsonify(added=True)
    except:
        return jsonify(added=False)


@app.route("/show/<int:show_id>/actors")
def show_actors(show_id):
    show = queries.get_show(show_id)
    actors = queries.get_show_characters(show_id)

    return render_template("actors.html", actors=actors, show=show)


@app.route("/edit_actor/<int:actor_id>", methods=["GET", "POST"])
def edit_actor(actor_id):
    if not "username" in session:
        return redirect(url_for("index"))
    if request.method == "GET":
        character = queries.get_character(actor_id)
        actor_id_from_character = character.get("actor_id")
        actor = queries.get_actor(actor_id_from_character)

        return render_template("edit_actor.html", actor=actor)
    else:
        try:
            data = ast.literal_eval(request.data.decode("utf-8"))
            queries.change_actor(data.get("actor_id"), data.get("actor_name"))
            return jsonify(changed=True)
        except:
            return jsonify(changed=False)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
