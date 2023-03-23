from django.shortcuts import render,get_object_or_404
from django.views.generic.base import TemplateView
from django.views import generic
from django.urls import reverse_lazy
from django.core.mail import send_mail
from . import forms
from . import models
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage,\
    PageNotAnInteger

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


def post_list(request, tag_slug=None):
    post_lists = models.Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_lists = post_lists.filter(tags__in=[tag])
    paginator = Paginator(post_lists, 5)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
    # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                    'blog/list.html',
                    {'posts': posts,
                    'tag': tag})


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