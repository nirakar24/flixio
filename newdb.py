import sqlite3
from pathlib import Path

# Connect to the merged database
merged_db_path = Path("merged_database.db")
conn_merged = sqlite3.connect(merged_db_path)
cursor_merged = conn_merged.cursor()

# Connect to the SQLite3 database
sqlite3_db_path = Path("db.sqlite3")
conn_sqlite3 = sqlite3.connect(sqlite3_db_path)
cursor_sqlite3 = conn_sqlite3.cursor()

# Select data from the merged database
cursor_merged.execute("SELECT title, description, release_date, genre, poster, background_poster, popularity, vote_count, vote_average, original_language, movie_id FROM movie")
movies_data = cursor_merged.fetchall()

# Insert data into the movies_movie table in SQLite3 database
for movie in movies_data:
    movie_id = movie[-1]  # Get the movie_id from the last element of the tuple
    # Check if the movie ID already exists in the movies_movie table
    cursor_sqlite3.execute("SELECT movie_id FROM movies_movie WHERE movie_id=?", (movie_id,))
    existing_movie = cursor_sqlite3.fetchone()
    if existing_movie is None:
        # If the movie ID doesn't exist, insert the movie data
        try:
            cursor_sqlite3.execute("""
                INSERT INTO movies_movie (
                    title, description, release_date, genre, poster, background_poster,
                    popularity, vote_count, vote_average, original_language, movie_id,
                    adult, streaming_url, trailer_id, sequence_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, NULL, NULL, 0)
            """, movie)
        except sqlite3.IntegrityError:
            print(f"Failed to insert movie with ID {movie_id}. IntegrityError occurred.")
    else:
        print(f"Movie with ID {movie_id} already exists. Skipping insertion.")

# Commit changes and close connections
conn_sqlite3.commit()
conn_sqlite3.close()
conn_merged.close()

print("Movies data has been successfully added to the movies_movie table.")
