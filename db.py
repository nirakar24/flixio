import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'streaming_platform.settings')
django.setup()

# Import the Movie model
from movies.models import Movie

# Retrieve all movies from the database
movies = Movie.objects.all()

# Initialize sequence_id
sequence_id = 1

# Update each movie with sequence_id
for movie in movies:
    movie.sequence_id = sequence_id
    movie.save()
    sequence_id += 1

print("Sequence IDs have been added to the movies_movie table.")
