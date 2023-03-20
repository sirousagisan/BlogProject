from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.

class home(TemplateView):
    template_name = "blog/home.html"

class about(TemplateView):
    template_name = "blog/about.html"