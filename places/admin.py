from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from places.models import Image, Place


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    readonly_fields = ('image_prewiew',)
    list_display = ('title', 'image_prewiew',)

    def image_prewiew(self, obj):
        html = '<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.url,
            width=obj.image.width / 6,
            height=obj.image.height / 6,
        )
        return format_html('{}', mark_safe(html))


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
