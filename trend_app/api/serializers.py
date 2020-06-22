from rest_framework import serializers
from trend_app.models import Trend, TrendName


class TrendNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendName
        fields = "__all__"

class TrendSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(queryset=TrendName.objects.all(), source='name.name')

    class Meta:
        model = Trend
        fields = "__all__"