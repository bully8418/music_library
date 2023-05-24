from .models import Playlist
from django import forms
from django.forms import ModelForm, CharField


class PlaylistCreate(ModelForm):
    class Meta:
        model = Playlist
        fields = ['list_name']






