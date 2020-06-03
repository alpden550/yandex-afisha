from django.urls import path

from places import views

app_name = 'pages'

urlpatterns = [
    path('', views.PlacesMainView.as_view(), name='index'),
    path('places/<int:pk>', views.PlaceDetailView.as_view(), name='place_detail'),
]
