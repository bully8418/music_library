from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, UserModel
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.base import View
from .models import *
from .forms import *
from django.db.models import Q, QuerySet
from hitcount.views import HitCountDetailView
from django.core.paginator import Paginator
from django.contrib import messages


class Search(ListView):
    model = Song
    template_name = 'sound/search_result.html'
    context_object_name = 'search'
    paginate_by = 1

    def get_queryset(self):
        return Song.objects.filter(
            Q(name__icontains=self.request.GET.get('q')) | Q(artist__name__icontains=self.request.GET.get('q')) | Q(
                album__name__icontains=self.request.GET.get('q'))
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f"q={self.request.GET.get('q')}&"
        return context


# main page where all music and content
class SongView(ListView):
    queryset = Song.objects.order_by('-date')[:3]
    template_name = 'base_page.html'
    context_object_name = 'music'
    paginate_by = 3

    def get_queryset(self):
        return Song.objects.all()

    # def get_context_data(self,  object_list=None, **kwargs):
    #     context = super() .get_context_data(**kwargs)
    #     context['s'] = f"s={self.request.GET.get('s')}&"
    #     return context


class SongDetailView(HitCountDetailView):
    model = Song
    template_name = 'sound/song_detail.html'
    context_object_name = 'rate'
    pk_url_kwarg = 'pk'
    # set to True to count the hit
    count_hit = True
    slug_field = "url"


class ArtistView(DetailView):
    model = Artist
    template_name = 'artists/artist_page.html'
    context_object_name = 'artist_info'


class AlbumsView(ListView):
    model = Album
    template_name = 'albums/albums_list.html'
    context_object_name = 'album_list'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(AlbumsView, self).get_context_data(**kwargs)
        context.update({
            'popular_albums': Album.objects.order_by('-hit_count_generic__hits')[:3],
        })
        return context


class ArtistsView(ListView):
    model = Artist
    template_name = 'artists/artists_list.html'
    context_object_name = 'artists'


class AlbumDetailView(HitCountDetailView):
    model = Album
    template_name = 'albums/album_page.html'
    context_object_name = 'album_info'
    pk_url_kwarg = 'pk'
    # set to True to count the hit
    count_hit = True


class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'test.html'
    success_url = reverse_lazy('home')


class UserProfile(DetailView):
    model = User
    template_name = 'users/user_profile.html'
    context_object_name = 'user_profile'


class UserPlaylist(DetailView):
    model = Playlist
    template_name = 'playlists/playlistsongs.html'
    context_object_name = 'user_playlist'


def add_track_to_playlist(request, pk):
    if request.method == 'POST':
        track_id = pk
        playlist_id = request.POST.get('playlist_id')
        track = Song.objects.get(pk=track_id)
        playlist = Playlist.objects.get(pk=playlist_id)
        if track in playlist.song.all():
            messages.success(request, 'Ужее имеется в плейлисте')
        else:
            playlist.song.add(track)
            messages.add_message(request, messages.SUCCESS, 'Успешно добавлен')
    return redirect(request.META['HTTP_REFERER'])


def new_songs(request):
    context = Song.objects.order_by('-date')[:3]
    return render(request, 'sound/new_songs.html', {'context': context})


# def new_playlist(request):
#     return render(request, 'playlists/createplaylist.html')


class PlaylistCRT(CreateView):
    template_name = 'playlists/createplaylist.html'
    form_class = PlaylistCreate
    model = Playlist.objects.all()
    success_url = reverse_lazy('home')









