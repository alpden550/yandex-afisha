from django.contrib import admin

from places.models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    """Register model Place in admin area."""

    list_display = ('id', 'title', 'latitude', 'longitude')
    list_filter = ('title',)
    search_fields = ('title', 'description_short')
