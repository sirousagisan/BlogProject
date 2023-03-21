from django.utils.safestring import mark_safe
from django import template
import markdown
from django.template.defaultfilters import stringfilter
from django.conf import settings
from ..models import Post

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag("blog/latest_posts.html")
def show_latest_posts(count=3):
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}

@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.filter
def markdown_to_html(text):
    """マークダウンをhtmlに変換する。"""
    html = markdown.markdown(text, extensions=settings.MARKDOWN_EXTENSIONS)
    return mark_safe(html)


@register.filter()
@stringfilter
def markdown_fil(value):
    return markdown.markdown(value, extensions=['markdown.extensions.fenced_code'])

@register.filter
@stringfilter
def markdown2html(value):
    return markdown.markdown(value)