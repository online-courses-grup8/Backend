from django.shortcuts import get_object_or_404
from blog.models import BlogPost


def get_published_posts():
    # yayınlanmış postları tarihe göre sıralı döner
    return BlogPost.objects.filter(is_published=True)


def get_post_by_slug(slug):
    # slug'a göre yayınlanmış post döner, yoksa 404
    return get_object_or_404(BlogPost, slug=slug, is_published=True)