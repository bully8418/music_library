# Generated by Django 4.1.1 on 2023-08-09 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music_library', '0008_artist_albums_alter_playlist_song'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='albums',
        ),
    ]