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
                    'placeId': 'placeId',
                    'detailsUrl': 'detailsUrl',
                },
            }
            places_geo.get('features').append(place_feature)

        context['places'] = places_geo
        return context


class PlaceDetailView(DetailView):
    model = Place
    template_name = "index.html"
