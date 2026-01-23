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
    print(user)

    cur.close()
    conn.close()

    if user and password == user[2]:
        return user
    elif user and password != user[2]:
        return False
    else:
        return None

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

def insert_movies(title, release_date, time, description):
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("""
               INSERT INTO movies(title, release_date, time, description) VALUES(%s, %s,%s,%s)
            """, (title, release_date, time, description))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    cur.close()
    conn.close()

def insert_review(user_id, movie_id, rate, review):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
               INSERT INTO actions (movie_id, user_id, type) 
               VALUES (%s,%s,'rate')
               RETURNING action_id
            """, (movie_id, user_id))

        action_id = cur.fetchone()[0]
        cur.execute("""
                INSERT INTO ratings (action_id, rating, review) 
                VALUES (%s,%s,%s)
            """, (action_id, rate, review))
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



if __name__ == "__main__":
    print(get_movies())
