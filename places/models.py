from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField


class Place(models.Model):
    """Model to represent a place object."""

    title = models.CharField('Title', max_length=250, unique=True, db_index=True)  # title must be unique too.
    place_id = models.SlugField('Place ID slug field', max_length=100, blank=True, unique=True)
    description_short = models.TextField('Short description', blank=True)
    description_long = HTMLField('Full description', blank=True)
    latitude = models.FloatField('Latitude')
    longitude = models.FloatField('Longitude')

    class Meta:
        verbose_name = 'Place'
        verbose_name_plural = 'Places'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """get absolute url for a place object."""
        return reverse("places:place_detail", kwargs={"pk": self.pk})


class Image(models.Model):
    """Image for a place object."""

    image = models.ImageField('Image')
    position = models.PositiveIntegerField('Position', default=1)
    place = models.ForeignKey(
        'places.Place',
        verbose_name='Place',
        on_delete=models.CASCADE,
        related_name='images',
    )

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        ordering = ('position',)

    def __str__(self):
        return f'Image with ID {self.pk}'
