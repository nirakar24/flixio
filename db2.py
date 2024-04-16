import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Define the languages to keep (in this case, Hindi and English)
languages_to_keep = ('hi', 'en')

# Delete movies with languages other than Hindi or English
cursor.execute("DELETE FROM movies_movie WHERE original_language NOT IN (?, ?)", languages_to_keep)

# Commit the changes
conn.commit()

# Close the connection
conn.close()

print("Movies not in Hindi or English have been deleted.")
