import datetime
import uuid

import django.utils.timezone
import os

from django.utils.text import slugify
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from six import python_2_unicode_compatible

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone


class Artist(models.Model):
    name = models.CharField(verbose_name='Никнейм', max_length=100, db_index=True)
    about = models.TextField(verbose_name='Об артисте')
    home_town = models.CharField(verbose_name='Родной город', max_length=50)
    birth_date = models.DateField(verbose_name='Дата рождения')
    genre = models.CharField(verbose_name='Жанр', max_length=100)
    poster = models.ImageField('Обложка', upload_to='%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('artist', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Артист'
        verbose_name_plural = 'Артисты'
        ordering = ['name']


@python_2_unicode_compatible
class Album(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name='Исполнитель', related_name='albums_all')
    year = models.DateField(verbose_name='Год выпуска')
    genre = models.CharField(verbose_name='Жанр', max_length=100)
    num_songs = models.IntegerField(verbose_name='Кол-во треков')
    description = models.TextField(verbose_name='Описание')
    label = models.CharField(verbose_name='Лейбл', max_length=100)
    poster = models.ImageField('Обложка', upload_to='%Y/%m/%d/', blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('album', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'
        ordering = ['name']


@python_2_unicode_compatible
class Song(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    artist = models.ManyToManyField(Artist, verbose_name='Исполнитель', related_name='song_artist')
    file = models.FileField(verbose_name='Трек', upload_to='%Y/%m/%d/')
    album = models.ForeignKey(Album, verbose_name='Альбом', on_delete=models.CASCADE, null=True, blank=True,
                              related_name='song_album')
    date = models.DateTimeField(verbose_name='Дата и время создания записи', auto_now_add=True)
    # slug = models.SlugField(unique=True, max_length=100, default=uuid.uuid1)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Трек'
        verbose_name_plural = 'Треки'
        ordering = ['name']






