from .models import Playlist
from django import forms
from django.forms import ModelForm, CharField


class PlaylistCreate(ModelForm):
    class Meta:
        model = Playlist
        fields = ['list_name', 'user']
        widgets = {
            'list_name': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.HiddenInput(attrs={'class': 'form-control'}),
                  }








