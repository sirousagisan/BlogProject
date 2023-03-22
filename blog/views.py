from django.shortcuts import render,get_object_or_404
from django.views.generic.base import TemplateView
from django.views import generic
from django.urls import reverse_lazy
from django.core.mail import send_mail
from . import forms
from . import models
from django.utils import timezone
from django.views.decorators.http import require_POST
import pytz

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
    comment = post.comments.filter(active=True)
    form = forms.CommentForm()
    return render(request,
                    'blog/detail.html',context={
                    'post': post, 
                    "comment": comment,
                    "form": form
                    })
    
class PostListView(generic.ListView):
    queryset = models.Post.published.all()
    context_object_name = "posts"
    paginate_by = 5
    template_name = "blog/list.html"


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(models.Post, id=post_id,
                        status=models.Post.Status.PUBLISHED)
    comment = None
    form = forms.CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, "blog/comment.html",
                context={
                    "post": post,
                    "form": form,
                    "comment": comment
                })