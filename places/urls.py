from django.urls import path

from places import views

app_name = 'pages'

urlpatterns = [
    path('', views.PagesMainView.as_view(), name='index'),
]
