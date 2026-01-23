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

def insert_movies(title, year_of_production, time, description):
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("""
               INSERT INTO movies(title, year_of_production, time, description) VALUES(%s, %s,%s,%s)
            """, (title, year_of_production, time, description))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    cur.close()
    conn.close()

def insert_review(user_id, movie_id, rate, date, review):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
               INSERT INTO reviews (user_id, movie_id, rate, date, review) 
               VALUES (%s,%s,%s,%s,%s)
            """, (user_id, movie_id, rate, date, review))

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f'Database error:{e}')
        raise e
    cur.close()
    conn.close()


if __name__ == "__main__":
    print(get_movies())
