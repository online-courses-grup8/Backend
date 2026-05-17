# core/views/stats.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from core.selectors.stats import get_site_stats


class SiteStatsView(APIView):
    # GET /api/v1/stats/ - site istatistiklerini döner
    permission_classes = [AllowAny]

    def get(self, request):
        stats = get_site_stats()
        return Response({
            "status": 200,
            "payload": stats,
            "errorMessage": None
        })