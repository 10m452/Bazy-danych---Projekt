import psycopg2

def get_conn():
    return psycopg2.connect(**DB_CONFIG)

DB_CONFIG = {
    "host" : "localhost",
    "database" : "***",
    "user" : "***",
    "password" : "***",
    "port": 5432
}

