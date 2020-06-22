from rest_framework.viewsets import ModelViewSet
from trend_app.models import TrendName, Trend
from .serializers import TrendNameSerializer, TrendSerializer
from django.shortcuts import get_object_or_404


class TrendViewSet(ModelViewSet):
    queryset = Trend.objects.all()
    serializer_class = TrendSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        get_name = self.request.query_params.get('name', None)
        get_type = self.request.query_params.get('type', None)

        if get_name and get_type:
            get_name = str(get_name).lower()
            get_type = str(get_type).lower()
            trend_name = get_object_or_404(TrendName, name=get_name, search_type=get_type)
            return qs.filter(name=trend_name)

        if get_name and not get_type:
            get_name = str(get_name).lower()
            trend_name = get_object_or_404(TrendName, name=get_name)
            return qs.filter(name=trend_name)

        return qs