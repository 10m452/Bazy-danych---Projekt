from server import get_conn

def create_user(nick, password):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (nick, password)
        VALUES (%s, %s)
        """, (nick, password))

    conn.commit()
    cur.close()
    conn.close()

def auth(nick, password):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id, nick, password FROM users WHERE nick=%s
        """, (nick,))
    user = cur.fetchone()

    cur.close()
    conn.close()

    if user and password == user[2]:
        return user
    elif user and password != user[2]:
        return False
    else:
        return None

def change_password(user_id, new_pass):
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("""
                   SELECT change_password(%s, %s);
                """, (user_id, new_pass))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f'Error when changing password: {e}')
        raise e
    finally:
        cur.close()
        conn.close()

def get_movies():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
           SELECT * FROM movies 
           """)
    movies = list(cur.fetchall())

    cur.close()
    conn.close()

    return movies

def insert_movies(title, release_date, runtime, description, actors, directors, country_l, genre_l):
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("""
               SELECT add_movie(%s,%s,%s,%s,%s,%s,%s,%s);
            """, (title, release_date, runtime, description, actors, directors, country_l, genre_l))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f'Error when adding movie: {e}')
        raise e
    finally:
        cur.close()
        conn.close()

def insert_review(user_id, movie_id, rate, review):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
               SELECT rate(%s, %s, %s, %s);
            """, (movie_id, user_id, rate, review))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f'Database error:{e}')
        raise e
    finally:
        cur.close()
        conn.close()

def delete_review(user_id, movie_id):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT delete_rating(%s, %s);
            """, (user_id, movie_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f'Database error:{e}')
        raise e
    finally:
        cur.close()
        conn.close()

def delete_from_list(user_id, movie_id, l_name):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
               SELECT delete_from_list(%s, %s, %s);
            """, (user_id, movie_id, l_name))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f'Database error:{e}')
        raise e
    finally:
        cur.close()
        conn.close()

def searchmovie(search):
    conn = get_conn()
    cur = conn.cursor()

    pat = f'%{search}%'

    cur.execute("""
           SELECT * FROM movies WHERE title ILIKE %s
           """, (pat,))
    movie = list(cur.fetchall())

    cur.close()
    conn.close()

    return movie

def movie_info(movie_id):
    conn = get_conn()
    cur = conn.cursor()


    cur.execute("""
           SELECT * FROM movies WHERE movie_id = %s
           """, (movie_id,))
    info = cur.fetchone()

    cur.close()
    conn.close()

    return info

def top_10():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
           SELECT * FROM top_10;
           """)
    top = cur.fetchall()

    cur.close()
    conn.close()

    return top

def actors(movie_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
           SELECT movie_cast(%s);
           """, (movie_id, ))
    cast = cur.fetchall()

    cur.close()
    conn.close()

    actr = ", ".join(r[0] for r in cast)

    return actr

def country(movie_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
           select c.country
	        from countries c natural join movies m
	        where m.movie_id = %s;
           """, (movie_id, ))
    c = cur.fetchall()

    ctr = ", ".join(r[0] for r in c)

    cur.close()
    conn.close()

    return ctr

def genre(movie_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
           select g.genre
	        from genres g natural join movies m
	        where m.movie_id = %s;
           """, (movie_id, ))

    g = cur.fetchall()

    cur.close()
    conn.close()

    genres = ", ".join(r[0] for r in g)

    return genres

def directors(movie_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
           SELECT movie_director(%s);
           """, (movie_id, ))
    dirs = cur.fetchall()

    cur.close()
    conn.close()

    d = ", ".join(r[0] for r in dirs)

    return d

def add_to_list(movie_id, user_id, list_name):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
               SELECT add_to_list(%s,%s,%s);
               """, (movie_id,user_id,list_name))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e

    cur.close()
    conn.close()

def users_lists(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
           SELECT DISTINCT list_name FROM watchlists NATURAL JOIN actions WHERE user_id = %s;
           """, (user_id, ))
    watchlists = cur.fetchall()
    wl = [w[0] for w in watchlists]

    cur.close()
    conn.close()
    return wl

def movies_on_list(name):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
           SELECT movie_id, title, release_date FROM actions NATURAL JOIN movies 
           NATURAL JOIN watchlists WHERE type LIKE 'list' AND list_name LIKE %s;
           """, (name, ))
    mov_on_watchlist = cur.fetchall()

    cur.close()
    conn.close()
    return mov_on_watchlist

def movies_from_country(c):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
           SELECT * FROM movies_from(%s);
           """, (c,))
    mov_l = cur.fetchall()

    cur.close()
    conn.close()

    return mov_l

def directors_movies(d):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
           SELECT * FROM director_movies(%s);
           """, (d,))
    mov_l = cur.fetchall()

    cur.close()
    conn.close()

    return mov_l

def movies_by_genre(g):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
           SELECT * FROM genre_movies(%s);
           """, (g,))
    mov_l = cur.fetchall()

    cur.close()
    conn.close()

    return mov_l

def movies_by_actor(a):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
           SELECT * FROM actor_movies(%s);
           """, (a,))
    mov_l = cur.fetchall()

    cur.close()
    conn.close()

    return mov_l

def get_all_genres():

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
           SELECT DISTINCT genre FROM genres ORDER BY genre;""")
    gen = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()

    return gen

def get_all_directors():

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
           SELECT DISTINCT name FROM people NATURAL JOIN people_movies WHERE people_movies.role ILIKE 'Director';""")
    gen = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()

    return gen

def get_all_countries():

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
           SELECT DISTINCT country FROM countries;""")
    gen = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()

    return gen

def get_all_actors():

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
           SELECT DISTINCT name FROM people NATURAL JOIN 
           people_movies WHERE people_movies.role ILIKE 'Actor';""")
    a = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()

    return a

def get_average_rate(movie_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
           SELECT * FROM movie_avg(%s);""", (movie_id, ))
    a = cur.fetchone()
    if a[0] is None:
        a = None
    cur.close()
    conn.close()

    return a

def show_watched(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
          SELECT * FROM show_watched(%s);
           """, (user_id, ))
    w = cur.fetchall()
    cur.close()
    conn.close()

    return w

def del_watched(user_id, movie_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
          SELECT * FROM delete_watched(%s, %s);
           """, (user_id, movie_id, ))
    conn.commit()
    cur.close()
    conn.close()

def show_movie_review(movie_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
          SELECT * FROM show_movie_reviews(%s);
           """, (movie_id, ))
    w = cur.fetchall()
    cur.close()
    conn.close()

    return w

def show_user_reviews(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
          SELECT * FROM show_user_reviews(%s);
           """, (user_id, ))
    w = cur.fetchall()
    cur.close()
    conn.close()

    return w

def mark_as_watched(movie_id, user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
          SELECT mark_as_watched(%s, %s);
           """, (movie_id, user_id))
    conn.commit()
    cur.close()
    conn.close()

def delete_rating(user_id, movie_id):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
           SELECT delete_rating(%s,%s);
           """, (user_id, movie_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f'Database error:{e}')
        raise e
    finally:
        cur.close()
        conn.close()
