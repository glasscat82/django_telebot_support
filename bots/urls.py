from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views


urlpatterns = [
    path("", csrf_exempt(views.main_view), name='main_view'),
    path("bots/<str:token>/", csrf_exempt(views.api_bots), name='api_bots'),
]
