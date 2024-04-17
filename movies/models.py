from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import *

class Movie(models.Model):
    sequence_id = models.IntegerField(default=1)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=100, null=True, blank=True)
    poster = models.ImageField(upload_to='movie_posters/', default='https://s.studiobinder.com/wp-content/uploads/2017/12/Movie-Poster-Template-Dark-with-Image.jpg?x81279')
    background_poster = models.ImageField(upload_to='background_posters/',default='https://t4.ftcdn.net/jpg/05/49/86/39/360_F_549863991_6yPKI08MG7JiZX83tMHlhDtd6XLFAMce.jpg')
    popularity = models.FloatField(null=True, blank=True)
    vote_count = models.IntegerField(null=True, blank=True)
    vote_average = models.FloatField(null=True, blank=True)
    original_language = models.CharField(max_length=100, null=True, blank=True)
    movie_id = models.IntegerField(primary_key=True)  # Assuming movie_id is the primary key
    adult = models.BooleanField(null=True, blank=True)
    trailer = models.ForeignKey('Trailer', on_delete=models.SET_NULL, null=True, blank=True)
    streaming_url = models.URLField(null=True, blank=True)

    class Meta:
        managed = True

class Trailer(models.Model):
    title = models.CharField(max_length=100)
    poster = models.ImageField(upload_to='trailers/posters/')
    video_url = models.URLField()

    def __str__(self):
        return self.title
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wishlist = models.ManyToManyField(Movie, blank=True)

    def __str__(self):
        return self.user.username
        

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

