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
