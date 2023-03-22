from django.urls import path
from . import views

app_name ="blog"

urlpatterns = [
    path("", views.home.as_view(), name="home"),
    path("about/", views.aboutView, name="about"),
    path("blog/", views.PostListView.as_view(), name="list"),
    path("blog/<int:year>/<int:month>/<int:day>/<slug:post>/",
                views.post_detail, name='post_detail'),
    path("<int:post_id>/comment",views.post_comment, name="post_comment")
]
