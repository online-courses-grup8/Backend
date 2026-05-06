from rest_framework import generics
from rest_framework.permissions import AllowAny
from core.serializers import FAQSerializer
from core.selectors import get_active_faqs


class FAQListView(generics.ListAPIView):
    permission_classes = [AllowAny]  # login olmadan erişilebilir
    serializer_class = FAQSerializer

    def get_queryset(self):
        return get_active_faqs()