from pathlib import Path

import requests
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile

from places.models import Image, Place

PLACES_JSON_URLS = [
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%90%D0%BD%D1%82%D0%B8%D0%BA%D0%B0%D1%84%D0%B5%20Bizone.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%90%D1%80%D1%82-%D0%BF%D1%80%D0%BE%D1%81%D1%82%D1%80%D0%B0%D0%BD%D1%81%D1%82%D0%B2%D0%BE%20%C2%AB%D0%91%D1%83%D0%BD%D0%BA%D0%B5%D1%80%20703%C2%BB.json',
]


class Command(BaseCommand):
    help = 'Create place object and images from extaernal json file.'

    def add_arguments(self, parser):
        parser.add_argument('-json_url', type=str, nargs='?')

    def handle(self, *args, **kwargs):
        if kwargs.get('json_url'):
            place_json = self.get_json_from_url(kwargs.get('json_url'))
            self.save_place(place_json)

    def save_place(self, place_data: dict):
        defaults = {}
        defaults['title'] = place_data.get('title')
        defaults['description_short'] = place_data.get('description_short')
        defaults['description_long'] = place_data.get('description_long')
        defaults['latitude'] = place_data.get('coordinates').get('lat')
        defaults['longitude'] = place_data.get('coordinates').get('lng')

        try:
            place, created = Place.objects.get_or_create(
                title=place_data.get('title'),
                defaults=defaults,
            )
        except IntegrityError as error:
            self.stdout.write(
                self.style.ERROR(
                    'Impossible to create place {place} – error "{error}"'.format(
                        place=place_data['title'], error=error,
                    ),
                ),
            )

        if created:
            images = place_data.get('imgs')
            for image in images:
                self.save_image(image, place)

            self.stdout.write(
                self.style.SUCCESS('Successfully created "{place}"'.format(place=place_data['title'])),
            )

    def save_image(self, image_url, place):
        image_name = Path(image_url).name
        try:
            image_content = self.get_image_binary_content(image_url)
        except requests.HTTPError:
            return
        image = Image(
            image=SimpleUploadedFile(image_name, image_content, content_type='image'),
            place=place,
        )
        image.save()

    @staticmethod
    def get_json_from_url(url: str):
        response = requests.get(url=url)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_image_binary_content(url: str):
        response = requests.get(url=url)
        response.raise_for_status()
        return response.content
