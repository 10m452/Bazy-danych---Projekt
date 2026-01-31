import csv
import psycopg2


# połączenie z bazą
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="***", # baza
    user="***",
    password="***" # haslo
)

cur = conn.cursor()

# import do tabeli movies
with open("movies_data.csv", encoding="cp1250") as f:

    reader = csv.reader(f)
    next(reader)  # jeśli plik ma nagłówek
    for row in reader:
        # Zamiana 'NA' na None
        row = [None if (x == 'NA' or x == '') else x for x in row]
        cur.execute(
            "INSERT INTO movies (movie_id, title, release_date, runtime, description) VALUES (%s, %s, %s, %s, %s)",
            row[:5]
        )

conn.commit()

# import do tabeli people
with open("people_data", encoding="cp1250") as f:

    reader = csv.reader(f)
    next(reader)
    for row in reader:
        # Zamiana 'NA' i '' na None (NULL)
        row = [None if (x == 'NA' or x == '') else x for x in row]
        cur.execute(
            "INSERT INTO people (person_id, name) VALUES (%s, %s)",
            row[:2]
        )
        
conn.commit()

# import do tabeli countries
with open("countries_data.csv", encoding="cp1250") as f:

    reader = csv.reader(f)
    next(reader)
    for row in reader:
        # Zamiana 'NA' i '' na None (NULL)
        row = [None if (x == 'NA' or x == '') else x for x in row]
        cur.execute(
            "INSERT INTO countries (movie_id, country) VALUES (%s, %s)",
            row[:2]
        )

conn.commit()

# import do tabeli genres
with open("genres_data.csv", encoding="cp1250") as f:

    reader = csv.reader(f)
    next(reader)
    for row in reader:
        # Zamiana 'NA' i '' na None (NULL)
        row = [None if (x == 'NA' or x == '') else x for x in row]
        cur.execute(
            "INSERT INTO genres (movie_id, genre) VALUES (%s, %s)",
            row[:2]
        )

conn.commit()


# import do tabeli people_movies (aktorzy)
with open("movies_actors_data", encoding="cp1250") as f:

    reader = csv.reader(f)
    next(reader)
    for row in reader:
        # Zamiana 'NA' i '' na None (NULL)
        row = [None if (x == 'NA' or x == '') else x for x in row]
        cur.execute(
            "INSERT INTO people_movies (movie_id, person_id, role) VALUES (%s, %s, %s)",
            row[:2] + row[3:]
        )

conn.commit()

# import do tabeli people_movies (tworcy)
with open("movies_crew_data", encoding="cp1250") as f:

    reader = csv.reader(f)
    next(reader)
    for row in reader:
        # Zamiana 'NA' i '' na None (NULL)
        row = [None if (x == 'NA' or x == '') else x for x in row]
        cur.execute(
            "INSERT INTO people_movies (movie_id, person_id, role) VALUES (%s, %s, %s)",
            row[:2] + row[3:]
        )


conn.commit()
cur.close()
conn.close()
