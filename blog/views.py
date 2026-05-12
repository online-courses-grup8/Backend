from rest_framework import generics
from rest_framework.permissions import AllowAny
from utils.pagination import CustomPageNumberPagination
from blog.serializers import BlogListSerializer
from blog.selectors import get_published_posts, get_post_by_slug


class BlogListView(generics.ListAPIView):
    # GET /api/v1/blog/ → yayınlanmış postları listeler
    permission_classes = [AllowAny]
    serializer_class = BlogListSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return get_published_posts()


