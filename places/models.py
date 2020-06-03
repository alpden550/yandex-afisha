from django.db import models
from django.urls import reverse


class Place(models.Model):
    """Model to represent place object."""

    title = models.CharField('Title', max_length=250, unique=True, db_index=True)
    place_id = models.CharField('Place ID slug field', max_length=100)
    description_short = models.TextField('Short description', blank=True)
    description_long = models.TextField('Full description', blank=True)
    latitude = models.FloatField('Latitude')
    longitude = models.FloatField('Longitude')

    class Meta:
        verbose_name = 'Place'
        verbose_name_plural = 'Places'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """get absolute url for palce object."""
        return reverse("places:place_detail", kwargs={"pk": self.pk})


class Image(models.Model):
    """Image for a place object."""

    image = models.ImageField('Image')
    place = models.ForeignKey(
        'places.Place',
        verbose_name='Place',
        on_delete=models.CASCADE,
        related_name='images',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return f'Image with ID {self.pk}'

    @property
    def get_image_url(self):
        """Get full image url to use in a view."""
        return "{}".format(self.image.url)
