import sqlite3

# Connect to the database
conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Delete movies with popularity < 30
cursor.execute("DELETE FROM movies_movie WHERE popularity < 30")
conn.commit()

# Fetch all remaining movies ordered by movie_id (or release_date if needed)
cursor.execute("SELECT movie_id FROM movies_movie ORDER BY movie_id ASC")
movies = cursor.fetchall()

# Update sequence_id in order
for i, (movie_id,) in enumerate(movies, start=1):
    cursor.execute("UPDATE movies_movie SET sequence_id = ? WHERE movie_id = ?", (i, movie_id))

# Commit changes and close connection
conn.commit()
conn.close()

print(f"Deleted movies with popularity < 30 and updated sequence IDs successfully!")
