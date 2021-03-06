from django.http import JsonResponse
from django.views.generic import DetailView, TemplateView

from places.models import Place


class PlacesMainView(TemplateView):
    """Manage main page."""

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        '''Pass into context places dict for js.'''
        places = Place.objects.all()
        context = super().get_context_data()

        places_geo = {
          'type': 'FeatureCollection',
          'features': [],
        }

        for place in places:
            place_feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [place.longitude, place.latitude],
                },
                'properties': {
                    'title': place.title,
                    'placeId': place.place_id,
                    'detailsUrl': place.get_absolute_url(),
                },
            }
            places_geo.get('features').append(place_feature)

        context['places'] = places_geo
        return context


class PlaceDetailView(DetailView):
    """Manage place detail object."""

    model = Place
    template_name = "index.html"

    def get_queryset(self):
        """Get queryset with related objects."""
        queryset = Place.objects.prefetch_related('images')
        return queryset

    def get(self, request, *args, **kwargs):
        """Pass serialized place object."""
        place = self.get_object()

        place_data = {
          'title': place.title,
          'description_short': place.description_short,
          'description_long': place.description_long,
          'coordinates': {
            'lat': place.latitude,
            'lng': place.longitude,
          },
          'imgs': [place_image.image.url for place_image in place.images.all()],
        }

        return JsonResponse(
            place_data,
            json_dumps_params={'ensure_ascii': False, 'indent': 4},
            safe=False,
        )
