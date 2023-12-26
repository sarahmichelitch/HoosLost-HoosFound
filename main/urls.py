from django.urls import path
from . import views

app_name = "LostandFound"
urlpatterns = [
    path("", views.index, name="index"),
]