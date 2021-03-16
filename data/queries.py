from data import data_manager
from psycopg2 import sql


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_show_count():
    return data_manager.execute_select('SELECT count(*) FROM shows;')


def get_shows_like(phrase):
    return data_manager.execute_select(
    sql.SQL(f"""
        SELECT 
            shows.id,
            shows.title
        FROM shows
        WHERE shows.title ILIKE '%{phrase}%'
        ORDER BY shows.title
    """))


def get_shows_limited(order_by="rating", order="DESC", limit=0, offset=0):
    return data_manager.execute_select(
        sql.SQL("""
            SELECT
                shows.id,
                shows.title,
                shows.year,
                shows.runtime,
                to_char(shows.rating::float, '999.9') AS rating_string,
                string_agg(genres.name, ', ' ORDER BY genres.name) AS genres_list,
                shows.trailer,
                shows.homepage
            FROM shows
                JOIN show_genres ON shows.id = show_genres.show_id
                JOIN genres ON show_genres.genre_id = genres.id
            GROUP BY shows.id
            ORDER BY
                CASE WHEN %(order)s = 'ASC' THEN {order_by} END ASC,
                CASE WHEN %(order)s = 'DESC' THEN {order_by} END DESC
            LIMIT %(limit)s
            OFFSET %(offset)s;
        """
                ).format(order_by=sql.Identifier(order_by)),
        {"order": order, "limit": limit, "offset": offset}
    )


def get_show(id):
    return data_manager.execute_select("""
        SELECT
            shows.id,
            shows.title,
            shows.year,
            shows.runtime,
            to_char(shows.rating::float, '999.9') AS rating_string,
            string_agg(genres.name, ', ' ORDER BY genres.name) AS genres_list,
            shows.trailer,
            shows.homepage,
            shows.overview
        FROM shows
            JOIN show_genres ON shows.id = show_genres.show_id
            JOIN genres ON show_genres.genre_id = genres.id
        WHERE shows.id = %(id)s
        GROUP BY shows.id;
    """, {"id": id}, False)


def get_show_characters(show_id):
    return data_manager.execute_select("""
        SELECT character_name, name, birthday, death, biography, a.id
        FROM actors a
        JOIN show_characters sc on a.id = sc.actor_id
        WHERE show_id = %(show_id)s
        ORDER BY a.id
    """, {"show_id": show_id})


def get_show_seasons(id):
    return data_manager.execute_select("""
        SELECT *
        FROM shows
        JOIN seasons ON shows.id = seasons.show_id
        WHERE shows.id = %(id)s;
    """, {"id": id})


def create_user(username, password):
    return data_manager.execute_select(
        sql.SQL("""
        INSERT INTO users (username, password) 
        VALUES ('{}', '{}')
        """.format(username, password)))


def get_username(username):
    return data_manager.execute_select(
        sql.SQL("""
        SELECT username
        FROM public.users
        WHERE username='{}'
        """.format(username))
    )


def get_user(username):
    return data_manager.execute_select(
        sql.SQL("""
        SELECT username, password
        FROM public.users
        WHERE username='{}'
        """.format(username))
    )


def get_all_shows_info():
    return data_manager.execute_select(
        sql.SQL("""
        SELECT * 
        FROM shows
        ORDER BY title""")
    )


def get_episodes(season_id):
    return data_manager.execute_select(
        sql.SQL("""
        SELECT *
        FROM episodes
        WHERE season_id = {}
        ORDER BY id
        """.format(season_id))
    )


def get_episode_details(episode_id):
    return data_manager.execute_select(
        sql.SQL("""
        SELECT *
        FROM episodes
        WHERE id = {}
        """.format(episode_id))
    )[0]


def update_episode(episode_id, title, overview):
    return data_manager.execute_dml_statement(
        """
        UPDATE episodes
        SET title = %(title)s, overview = %(overview)s
        WHERE id = %(id)s
        """, {"title": title, "overview": overview, "id": episode_id}
    )


def get_episodes(season_id):
    return data_manager.execute_select(
        sql.SQL("""
        SELECT *
        FROM episodes
        WHERE season_id = {}
        ORDER BY id
        """.format(season_id))
    )


def get_season(season_id):
    return data_manager.execute_select(
        sql.SQL("""
        SELECT *
        FROM seasons
        WHERE id = {}
        """.format(season_id))
    )


def add_episode(season_id, episode_number, title, overview):
    return data_manager.execute_dml_statement(
        """
        INSERT INTO episodes
        (title, episode_number, overview, season_id)
        VALUES 
        (%(title)s, %(episode_number)s, %(overview)s, %(season_id)s)
        """, {"title": title, "overview": overview, "episode_number": episode_number, "season_id": season_id}
    )


def add_season(season_number, title, overview, show_id):
    return data_manager.execute_dml_statement(
        """
        INSERT INTO seasons
        (season_number, title, overview, show_id) 
        VALUES 
        (%(season_number)s, %(title)s, %(overview)s, %(show_id)s)
        """,
        {"season_number": season_number, "title": title, "overview": overview, "show_id": show_id}
    )


def get_character(actor_id):
    return data_manager.execute_select(
        """
            SELECT * 
            FROM show_characters
            WHERE show_characters.actor_id=%(actor_id)s
            
        """, {"actor_id": actor_id}, fetchall=False)


def get_actor(actor_id):
    return data_manager.execute_select(
        """
        SELECT *
        FROM actors
        WHERE id=%(actor_id)s
        """, {"actor_id": actor_id}, fetchall=False
    )


def change_actor(actor_id, new_name):
    return data_manager.execute_dml_statement(
        """
        UPDATE actors
        SET name = %(new_name)s
        WHERE actors.id = %(actor_id)s
        """, {"actor_id": actor_id, "new_name": new_name}
    )