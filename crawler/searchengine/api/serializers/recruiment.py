from rest_framework import serializers

from api import models
from api.serializers.base import (
 RangeSerializer,
 SearchBaseSerializer,
 ResultSearchBaseSerializer
)


class SearchRecruimentSerializer(SearchBaseSerializer):
    source = serializers.ListField(
        child=serializers.IntegerField(),
        required=False, allow_null=True, allow_empty=True
        )
    search = serializers.CharField(required=False, allow_null=True)
    category = serializers.CharField(required=False, allow_null=True)
    sub_category = serializers.CharField(required=False, allow_null=True)
    province = serializers.CharField(required=False, allow_null=True)
    city = serializers.CharField(required=False, allow_null=True)
    salary=RangeSerializer(required=False)
    time=serializers.IntegerField(required=False)
    gender=serializers.ListField(
        child=serializers.CharField(),
        required=False, allow_null=True, allow_empty=True
        )
    cooperation=serializers.ListField(
        child=serializers.CharField(),
        required=False, allow_null=True, allow_empty=True
        )
    experience=RangeSerializer(required=False)
    education=serializers.ListField(
        child=serializers.CharField(),
        required=False, allow_null=True, allow_empty=True
        )
    insurnace=serializers.ListField(
        child=serializers.CharField(),
        required=False, allow_null=True, allow_empty=True
        )


class RecruimentSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.RecruimentAds
        fields = '__all__'


class ResultSearchRecruimentSerializer(ResultSearchBaseSerializer):
    class Meta:
        model = models.RecruimentAds
        fields = '__all__'


class RecruimentAdWithSimilar(ResultSearchBaseSerializer):
    similar = ResultSearchRecruimentSerializer(many=True, read_only=True)

    class Meta:
        model = models.RecruimentAds
        fields = '__all__'


class FavouriteResultRecruiment(ResultSearchRecruimentSerializer):
    favourite = None
    cat_type = serializers.ReadOnlyField(default='recruiment')

    class Meta:
        model = models.RecruimentAds
        fields = '__all__'
