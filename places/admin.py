from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from places.models import Image, Place

IMAGE_THUMB_WIDTH = 150


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    """Register inlines images for a place object."""

    model = Image
    list_display = ('title', 'image_prewiew',)
    readonly_fields = ('image_prewiew',)
    extra = 0

    def image_prewiew(self, obj):
        image = obj.image.url
        return format_html('<img src="{}" width={} />', image, IMAGE_THUMB_WIDTH)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    """Register model Place in admin area."""

    list_display = ('id', 'title', 'latitude', 'longitude')
    list_display_links = ('title',)
    list_filter = ('title',)
    search_fields = ('title', 'description_short')

    inlines = [
        ImageInline,
    ]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """Register Images in admin area."""

    list_filter = ('place',)
    raw_id_fields = ('place', )
