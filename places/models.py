from django.conf import settings
from django.db import models


class Place(models.Model):
    """Model to represent place object."""

    title = models.CharField('Title', max_length=250, unique=True, db_index=True)
    description_short = models.TextField('Short description', blank=True)
    description_long = models.TextField('Full description', blank=True)
    latitude = models.FloatField('Latitude')
    longitude = models.FloatField('Longitude')

    class Meta:
        verbose_name = 'Place'
        verbose_name_plural = 'Places'

    def __str__(self):
        return self.title


class Image(models.Model):
    """Image for a place object."""

    image = models.ImageField('Image', upload_to=settings.UPLOAD_IMAGE_PATH)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return f'Image with ID {self.pk}'
