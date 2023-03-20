from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from . import forms

# Create your views here.

class home(TemplateView):
    template_name = "blog/home.html"

class about(TemplateView):
    template_name = "blog/about.html"

def aboutView(request):
    sent = False
    if request.method == "POST":
        form = forms.aboutForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = "Kato's siteから"
            message = "フォームの利用ありがとうございます。"
            send_mail(subject, message, "katopillow@gmail.com", [cd["email"]])
            sent = True
    else:
        form = forms.aboutForm()
    return render(request, "blog/about.html", context={
        "form": form,
        "sent": sent
    })
