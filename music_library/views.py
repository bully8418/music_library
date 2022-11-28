from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import *
from .forms import *
from django.db.models import Q, QuerySet
from hitcount.views import HitCountDetailView
from django.core.paginator import Paginator


class Search(ListView):
    model = Song
    template_name = 'search_result.html'
    context_object_name = 'search'
    paginate_by = 1

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query:
            query = query.capitalize()
            object_list = Song.objects.filter(
                Q(name__icontains=query) | Q(artist__name__icontains=query) | Q(album__name__icontains=query)
            )
            return object_list
        return Song.objects.all()


# main page where all music and content
class SongView(ListView):
    queryset = Song.objects.order_by('-date')[:3]
    template_name = 'base_page.html'
    context_object_name = 'music'
    paginate_by = 1


class SongDetailView(HitCountDetailView):
    model = Song
    template_name = 'song_detail.html'
    context_object_name = 'rate'
    pk_url_kwarg = 'pk'
    # set to True to count the hit
    count_hit = True
    slug_field = "url"


class ArtistView(DetailView):
    model = Artist
    template_name = 'artist_page.html'
    context_object_name = 'artist_info'


class AlbumsView(ListView):
    model = Album
    template_name = 'albums_list.html'
    context_object_name = 'album_list'


class ArtistsView(ListView):
    model = Artist
    template_name = 'artists_list.html'
    context_object_name = 'artists'


class AlbumDetailView(HitCountDetailView):
    model = Album
    template_name = 'album_page.html'
    context_object_name = 'album_info'
    pk_url_kwarg = 'pk'
    # set to True to count the hit
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(AlbumDetailView, self).get_context_data(**kwargs)
        context.update({
            'popular_albums': Album.objects.order_by('-hit_count_generic__hits')[:3],
        })
        return context



