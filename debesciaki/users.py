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

    if not user:
        create_user(nick,password)

    return None
