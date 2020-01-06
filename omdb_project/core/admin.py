from django.contrib import admin

from core import models
# Register your models here.

admin.site.register(models.FavouriteMovie)
admin.site.register(models.MovieToWatch)
admin.site.register(models.Review)
