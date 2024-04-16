from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('movie/<int:movie_id>/', movie_details, name='movie_details'),
    path('add_to_wishlist/<int:movie_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('profile/', profile, name='profile'),
    path('all_movies/', all_movies, name='all_movies'),

]