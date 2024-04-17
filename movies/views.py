from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from datetime import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def recommend_movies(movie, num_recommendations=10):
    # Fetch all Hindi and English movies from the database
    all_movies = Movie.objects.filter(original_language__in=['en', 'hi'])

    # Extract features from all movies
    movie_descriptions = [m.description for m in all_movies]
    movie_genres = [m.genre for m in all_movies]
    movie_titles = [m.title for m in all_movies]
    movie_popularities = [m.popularity for m in all_movies]
    movie_vote_averages = [m.vote_average for m in all_movies]

    # Combine features into a single string for each movie
    combined_features = [f"{title} {desc} {genre} {popularity} {vote_average}" for title, desc, genre, popularity, vote_average in zip(movie_titles, movie_descriptions, movie_genres, movie_popularities, movie_vote_averages)]

    # Compute TF-IDF vectors
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(combined_features)

    # Calculate cosine similarities
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Find index of the current movie
    current_movie_index = movie.sequence_id - 1  # Assuming movie IDs start from 1

    # Get similarity scores for all movies
    sim_scores = list(enumerate(cosine_similarities[current_movie_index]))

    # Sort movies based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get indices of recommended movies (excluding the current movie)
    recommended_indices = [index for index, _ in sim_scores[1:num_recommendations+1]]

    # Get recommended movies from database
    recommended_movies = [all_movies[index] for index in recommended_indices]

    return recommended_movies


def home(request):
    # Calculate the date 60 days ago from today
    sixty_days_ago = datetime.now().date() - timedelta(days=60)

    # Query English and Hindi movies released in the last 60 days
    latest_releases = Movie.objects.filter(
        release_date__gte=sixty_days_ago, 
        release_date__lte=datetime.now().date(),
        original_language__in=['en', 'hi']
    ).order_by('-release_date')[:10]

    # Query the top 3 English and Hindi movies released in the last 60 days with the highest popularity score
    spotlight_movies = Movie.objects.filter(
        release_date__gte=sixty_days_ago, 
        release_date__lte=datetime.now().date(),
        original_language__in=['en', 'hi']
    ).order_by('-popularity')[:5]

    trending_movies = Movie.objects.order_by('-popularity', '-vote_average')[:10]

    return render(request, 'home.html', {'latest_releases': latest_releases, 'spotlight_movies': spotlight_movies, 'trending_movies': trending_movies})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Replace 'home' with the name of your home page URL
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')  # Replace 'home' with the name of your home page URL

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Replace 'login' with the name of your login page URL
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    wishlisted_movies = user_profile.wishlist.all()
    return render(request, 'profile.html', {'movies': wishlisted_movies})


@login_required
def add_to_wishlist(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_profile.wishlist.add(movie)
    # messages.success(request, f'{movie.title} has been added to your wishlist.', extra_tags='alert')
    return redirect('movie_details', movie_id=movie_id)

def movie_details(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    trailers = [movie.trailer] if movie.trailer else []  
    sixty_days_ago = datetime.now().date() - timedelta(days=60)

    # Query English and Hindi movies released in the last 60 days
    latest_releases = Movie.objects.filter(
        release_date__gte=sixty_days_ago, 
        release_date__lte=datetime.now().date(),
        original_language__in=['en', 'hi']
    ).order_by('-release_date')[:10]

    recommendations = recommend_movies(movie)

    return render(request, 'movie_details.html', {'movie': movie, 'trailers': trailers, 'latest_releases':recommendations})

def all_movies(request):
    # Get all movies from the database
    movies = Movie.objects.all()
    print(len(movies))

    # Sorting functionality based on user selection
    sort_by = request.GET.get('sort_by')
    if sort_by == 'release_date':
        movies = movies.order_by('-release_date')
    elif sort_by == 'popularity':
        movies = movies.order_by('-popularity')
    elif sort_by == 'vote_average':
        movies = movies.order_by('-vote_average')

    # Language filter
    language = request.GET.get('language')
    if language == 'hi':
        movies = movies.filter(Q(original_language='hi') | Q(original_language='hin'))
    elif language == 'en':
        movies = movies.filter(Q(original_language='en') | Q(original_language='eng'))

    search_query = request.GET.get('search')
    if search_query:
        movies = movies.filter(title__icontains=search_query)

    movies_per_page = 20

    paginator = Paginator(movies, movies_per_page)

    page = request.GET.get('page')

    try:
        movies_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        movies_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        movies_page = paginator.page(paginator.num_pages)

    context = {
        'movies': movies_page,
        'movies_per_page': movies_per_page,
        'sort_by': sort_by,
        'language': language,
        'search_query': search_query
    }
    return render(request, 'all_movies.html', context)