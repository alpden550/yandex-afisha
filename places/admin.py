from django.contrib import admin

from places.models import Place, Image


class ImageInline(admin.TabularInline):
    model = Image


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    """Register model Place in admin area."""

    list_display = ('id', 'title', 'latitude', 'longitude')
    list_filter = ('title',)
    search_fields = ('title', 'description_short')

    inlines = [
        ImageInline,
    ]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """Register Images in admin area."""
