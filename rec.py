import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Connect to SQLite database
conn = sqlite3.connect('db.sqlite3')

# Load data from the movie table
query = "SELECT title, description, genre, release_date, popularity, vote_average, original_language FROM movies_movie"
data = pd.read_sql(query, conn)

# Drop rows with missing values
data = data.dropna()

# Feature engineering: combine relevant columns into a single text column
data['combined_features'] = data['title'] + ' ' + data['description'] + ' ' + data['genre'] + ' ' + \
                             data['popularity'].astype(str) + ' ' + data['vote_average'].astype(str)

# Initialize TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit and transform the combined features
tfidf_matrix = tfidf_vectorizer.fit_transform(data['combined_features'])

# Calculate cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

def recommend_movies(movie_title, language='en', top_n=10):
    # Get the index of the movie that matches the title
    idx = data[data['title'] == movie_title].index[0]

    # Get the pairwise similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top similar movies
    sim_scores = sim_scores[1:top_n+1]  # Exclude the input movie itself

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Filter movies by language
    similar_movies = data.iloc[movie_indices].loc[(data['original_language'] == language) | (data['original_language'] == 'hi')]

    return similar_movies[['title', 'description', 'release_date', 'genre', 'popularity', 'vote_average']]

# Example usage:
recommended_movies = recommend_movies("Iron Man", language='en')  # Example for English movies
print("Recommended English Movies:")
print(recommended_movies)

recommended_movies_hindi = recommend_movies("3 Idiots", language='hi')  # Example for Hindi movies
print("\nRecommended Hindi Movies:")
print(recommended_movies_hindi)
