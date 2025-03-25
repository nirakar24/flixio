import sqlite3

# Default images (if missing)
DEFAULT_POSTER = "https://s.studiobinder.com/wp-content/uploads/2017/12/Movie-Poster-Template-Dark-with-Image.jpg?x81279"
DEFAULT_BACKGROUND_POSTER = "https://t4.ftcdn.net/jpg/05/49/86/39/360_F_549863991_6yPKI08MG7JiZX83tMHlhDtd6XLFAMce.jpg"

# Connect to the source (neo.db) and destination (db.sqlite3) databases
neo_conn = sqlite3.connect("neo.db")
neo_cursor = neo_conn.cursor()

django_conn = sqlite3.connect("db.sqlite3")
django_cursor = django_conn.cursor()

# Fetch data from neo.db
neo_cursor.execute("SELECT * FROM movies")
movies = neo_cursor.fetchall()

# Get column names from neo.db
neo_cursor.execute("PRAGMA table_info(movies)")
columns = [col[1] for col in neo_cursor.fetchall()]

# Fetch the current max sequence_id from movies_movie
django_cursor.execute("SELECT MAX(sequence_id) FROM movies_movie")
max_sequence_id = django_cursor.fetchone()[0] or 0  # Default to 0 if table is empty

# Get existing movie_ids from movies_movie to avoid duplicates
django_cursor.execute("SELECT movie_id FROM movies_movie")
existing_movie_ids = {row[0] for row in django_cursor.fetchall()}  # Store as a set for fast lookup

# Rename "trailer" to "trailer_id" to match movies_movie schema
columns = ["trailer_id" if col == "trailer" else col for col in columns]

# Prepare insert query
columns_str = ", ".join(columns).replace("sequence_id,", "")  # Exclude sequence_id
placeholders = ", ".join(["?" for _ in columns if _ != "sequence_id"])
insert_query = f"INSERT INTO movies_movie (sequence_id, {columns_str}) VALUES (?, {placeholders})"

# Append data to movies_movie, skipping duplicates
new_movie_count = 0
for i, movie in enumerate(movies, start=max_sequence_id + 1):
    movie_dict = dict(zip(columns, movie))  # Convert tuple to dictionary
    movie_id = movie_dict["movie_id"]

    if movie_id in existing_movie_ids:
        print(f"Skipping duplicate movie_id: {movie_id}")
        continue  # Skip if already in the database

    # Ensure poster and background_poster are not NULL
    if not movie_dict.get("poster"):
        movie_dict["poster"] = DEFAULT_POSTER
    if not movie_dict.get("background_poster"):
        movie_dict["background_poster"] = DEFAULT_BACKGROUND_POSTER

    values = [i] + [movie_dict[col] if col != "trailer_id" else None for col in columns if col != "sequence_id"]
    django_cursor.execute(insert_query, values)
    new_movie_count += 1

# Commit changes and close connections
django_conn.commit()
neo_conn.close()
django_conn.close()

print(f"Data successfully appended! {new_movie_count} new movies added.")
