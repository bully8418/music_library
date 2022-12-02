from .views import *
from django.urls import path, include

urlpatterns = [
    path('', SongView.as_view(), name='home'),
    path('artist/<int:pk>/', ArtistView.as_view(), name='artist'),
    path('album/<int:pk>/', AlbumDetailView.as_view(), name='album'),
    path('search/', Search.as_view(), name='search'),
    path('<int:pk>/', SongDetailView.as_view(), name='detail'),
    path('albums/', AlbumsView.as_view(), name='albums'),
    path('artists/', ArtistsView.as_view(), name='artists'),
    # path('login/', LoginView.as_view(), name='login'),
    path("register/", RegisterUser.as_view(), name='register'),
    # path('profile/<int:pk>/', UserProfile.as_view(), name='userprofile')
]



