# Generated by Django 5.0.3 on 2024-04-16 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_trailer_movie_streaming_url_movie_trailer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='sequence_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
