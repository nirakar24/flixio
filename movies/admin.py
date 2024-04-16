from django.contrib import admin
from .models import *

class MovieAdmin(admin.ModelAdmin):
    search_fields = ['title','movie_id']

admin.site.register(Movie, MovieAdmin)

