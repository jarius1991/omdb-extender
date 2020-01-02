from django.urls import path, include

from rest_framework.routers import DefaultRouter

from movies import views

app_name = 'movie'

router = DefaultRouter()
router.register('to-watch', views.MovieToWatchViewSet)
router.register('favourite', views.FavouriteMovieViewSet)
router.register('review', views.ReviewViewSet)
router.register('', views.MovieViewSet, basename='movie')

urlpatterns = [
    path('', include(router.urls))
]
