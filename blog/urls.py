from django.urls import path
from . import views

app_name ="blog"

urlpatterns = [
    path("", views.home.as_view(), name="home"),
    path("about/", views.aboutView, name="about")
]
