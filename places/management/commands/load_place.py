from pathlib import Path

import requests
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.core.files.uploadedfile import SimpleUploadedFile

from places.models import Image, Place

PLACES_JSON_URLS = [
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%90%D0%BD%D1%82%D0%B8%D0%BA%D0%B0%D1%84%D0%B5%20Bizone.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%90%D1%80%D1%82-%D0%BF%D1%80%D0%BE%D1%81%D1%82%D1%80%D0%B0%D0%BD%D1%81%D1%82%D0%B2%D0%BE%20%C2%AB%D0%91%D1%83%D0%BD%D0%BA%D0%B5%D1%80%20703%C2%BB.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%92%D0%BE%D0%B4%D0%BE%D0%BF%D0%B0%D0%B4%20%D0%A0%D0%B0%D0%B4%D1%83%D0%B6%D0%BD%D1%8B%D0%B9.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%92%D0%BE%D1%80%D0%BE%D0%B1%D1%8C%D1%91%D0%B2%D1%8B%20%D0%B3%D0%BE%D1%80%D1%8B.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%93%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D1%82%D0%BE%D1%80%20%D0%9C%D0%B0%D1%80%D0%BA%D1%81%D0%B0%20%D0%B8%D0%BB%D0%B8%20%C2%AB%D0%9A%D0%B0%D1%82%D1%83%D1%88%D0%BA%D0%B0%20%D0%A2%D0%B5%D1%81%D0%BB%D0%B0%C2%BB.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%93%D0%BE%D1%80%D0%B1%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%93%D0%AD%D0%A1.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%94%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B0%D0%BB%20%D0%A4%D0%BB%D0%B0%D0%BA%D0%BE%D0%BD.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%94%D0%BE%D0%BC%2C%20%D0%B3%D0%B4%D0%B5%20%D1%81%D0%BD%D0%B8%D0%BC%D0%B0%D0%BB%D1%81%D1%8F%20%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%20%C2%AB%D0%9F%D0%BE%D0%BA%D1%80%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B5%20%D0%B2%D0%BE%D1%80%D0%BE%D1%82%D0%B0%C2%BB.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%97%D0%B0%D0%B1%D1%80%D0%BE%D1%88%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9%20%D0%BF%D0%B8%D0%BE%D0%BD%D0%B5%D1%80%D1%81%D0%BA%D0%B8%D0%B9%20%D0%BB%D0%B0%D0%B3%D0%B5%D1%80%D1%8C%20%C2%AB%D0%91%D0%B5%D0%BB%D0%BE%D0%B5%20%D0%BE%D0%B7%D0%B5%D1%80%D0%BE%C2%BB.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%97%D0%B0%D0%B1%D1%80%D0%BE%D1%88%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9%20%D0%BF%D0%B8%D0%BE%D0%BD%D0%B5%D1%80%D1%81%D0%BA%D0%B8%D0%B9%20%D0%BB%D0%B0%D0%B3%D0%B5%D1%80%D1%8C%20%C2%AB%D0%A1%D0%BA%D0%B0%D0%B7%D0%BA%D0%B0%C2%BB.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%98%D1%81%D1%82%D0%BE%D1%87%D0%BD%D0%B8%D0%BA%20%D0%9F%D1%80%D0%B5%D0%BF%D0%BE%D0%B4%D0%BE%D0%B1%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%A1%D0%B5%D1%80%D0%B3%D0%B8%D1%8F%20%D0%A0%D0%B0%D0%B4%D0%BE%D0%BD%D0%B5%D0%B6%D1%81%D0%BA%D0%BE%D0%B3%D0%BE.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%9A%D0%BE%D0%B2%D0%BE%D1%80%D0%BA%D0%B8%D0%BD%D0%B3%20Gravity.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%9A%D1%80%D0%B5%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%BE%D1%81%D1%82%D1%80%D0%B0%D0%BD%D1%81%D1%82%D0%B2%D0%BE%20%C2%AB%D0%9B%D1%8E%D0%BC%D1%8C%D0%B5%D1%80-%D0%A5%D0%BE%D0%BB%D0%BB%C2%BB.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%9B%D0%B0%D0%B3%D0%B5%D1%80%D1%8C%20%C2%AB%D0%9F%D0%BE%D0%B4%D0%BC%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D0%BD%D1%8B%D0%B9%C2%BB.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%9B%D0%BE%D0%BF%D0%B0%D1%82%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9%20%D1%80%D1%83%D0%B4%D0%BD%D0%B8%D0%BA.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%9C%D0%B5%D1%81%D1%82%D0%B0%2C%20%D0%B3%D0%B4%D0%B5%20%D1%81%D0%BD%D0%B8%D0%BC%D0%B0%D0%BB%D1%81%D1%8F%20%20%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%20%C2%AB%D0%9E%D0%BF%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D1%8F%20%E2%80%9E%D0%AB%E2%80%9C%20%D0%B8%C2%A0%D0%B4%D1%80%D1%83%D0%B3%D0%B8%D0%B5%20%D0%BF%D1%80%D0%B8%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D1%8F%20%D0%A8%D1%83%D1%80%D0%B8%D0%BA%D0%B0%C2%BB.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%9C%D0%BD%D0%BE%D0%B3%D0%BE%D1%84%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%87%D0%BD%D1%8B%D0%B9%20%D0%BB%D0%BE%D1%84%D1%82%20TelePort360%C2%B0.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%9C%D1%83%D0%B7%D0%B5%D0%B9%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20%D0%B8%D1%81%D1%82%D0%BE%D1%80%D0%B8%D0%B9.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%9E%D1%81%D1%82%D0%B0%D0%BD%D0%BA%D0%B8%D0%BD%D1%81%D0%BA%D0%B0%D1%8F%20%D1%82%D0%B5%D0%BB%D0%B5%D0%B1%D0%B0%D1%88%D0%BD%D1%8F.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%9F%D0%B0%D0%B2%D0%B8%D0%BB%D1%8C%D0%BE%D0%BD%20%C2%AB%D0%9A%D0%BE%D1%81%D0%BC%D0%BE%D1%81%C2%BB%20%D0%BD%D0%B0%20%D0%92%D0%94%D0%9D%D0%A5.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%9F%D0%B5%D1%89%D0%B5%D1%80%D1%8B%20%D0%A1%D1%8C%D1%8F%D0%BD%D1%8B.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%9F%D0%BB%D0%BE%D1%89%D0%B0%D0%B4%D0%BA%D0%B0%20%D0%B4%D0%BB%D1%8F%20%D1%81%D0%B2%D0%B8%D0%B4%D0%B0%D0%BD%D0%B8%D0%B9%20%D0%BD%D0%B0%2060-%D0%BC%20%D1%8D%D1%82%D0%B0%D0%B6%D0%B5%20%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0-%D0%A1%D0%B8%D1%82%D0%B8.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%A1%D0%BC%D0%BE%D1%82%D1%80%D0%BE%D0%B2%D0%B0%D1%8F%20%D0%BF%D0%BB%D0%BE%D1%89%D0%B0%D0%B4%D0%BA%D0%B0%20PANORAMA360%20%D0%B2%C2%A0%D0%9C%D0%9C%D0%94%D0%A6%20%C2%AB%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0-%D0%A1%D0%B8%D1%82%D0%B8%C2%BB.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%A1%D0%BC%D0%BE%D1%82%D1%80%D0%BE%D0%B2%D0%B0%D1%8F%20%D0%BF%D0%BB%D0%BE%D1%89%D0%B0%D0%B4%D0%BA%D0%B0%20%C2%AB%D0%92%D1%8B%D1%88%D0%B5%20%D0%A2%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE%20%D0%9B%D1%8E%D0%B1%D0%BE%D0%B2%D1%8C%C2%BB.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%AD%D0%B9%D1%84%D0%B5%D0%BB%D0%B5%D0%B2%D0%B0%20%D0%B1%D0%B0%D1%88%D0%BD%D1%8F%20%D0%B2%20%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B5.json',
    'https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/places/%D0%AF%D0%BF%D0%BE%D0%BD%D1%81%D0%BA%D0%B8%D0%B9%20%D1%81%D0%B0%D0%B4.json',
]


class Command(BaseCommand):
    help = 'Create place object and images from extaernal json file.'

    def add_arguments(self, parser):
        parser.add_argument('--json_url', type=str, nargs='?')
        parser.add_argument('--batch', '-B', action='store_true')

    def handle(self, *args, **kwargs):
        place_urls = []
        if kwargs.get('json_url'):
            place_urls.append(kwargs.get('json_url'))

        if kwargs.get('batch'):
            place_urls.extend(PLACES_JSON_URLS)

        for url in place_urls:
            try:
                place_json = self.get_json_from_url(url)
                self.save_place(place_json)
            except requests.HTTPError as error:
                self.stdout.write(
                    self.style.ERROR(error),
                )

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
