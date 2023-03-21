from django.shortcuts import render,get_object_or_404
from django.views.generic.base import TemplateView
from django.views import generic
from django.urls import reverse_lazy
from django.core.mail import send_mail
from . import forms
from . import models

# Create your views here.

class home(TemplateView):
    template_name = "blog/home.html"


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

def post_detail(request, year, month, day, post):
    post = get_object_or_404(models.Post,
    status=models.Post.Status.PUBLISHED,
    slug=post,
    publish__year=year,
    publish__month=month,
    publish__day=day)
    return render(request,
                    'blog/detail.html',context={
                    'post': post, 
                    })
    
class PostListView(generic.ListView):
    queryset = models.Post.published.all()
    context_object_name = "posts"
    paginate_by = 5
    template_name = "blog/list.html"