from django.utils import timezone
from rest_framework import serializers

from api import models, serializers as api_serializers


class GetActiveSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ActiveSearch
        exclude = (
        'filter',
        )


class SetActiveSearchSerializer(serializers.ModelSerializer):
    days = serializers.IntegerField(required=True, min_value=1)
    type = serializers.ChoiceField(
    required=True,
    choices=(
    ('recruiment', 'recruiment'),
    )
    )

    class Meta:
        model = models.ActiveSearch
        exclude = (
            'user',
            'create_time',
            'expire_time',
            'last_checked',
            'raw_filter'
            )

    def validate(self, attrs):
        attrs = super(SetActiveSearchSerializer, self).validate(attrs)
        if attrs.get('filter').get('time', False):
            attrs.get('filter').pop('time')
        if attrs.get('type') == 'recruiment':
            fltr = attrs.pop('filter')
            srl = api_serializers.SearchRecruimentSerializer(data=fltr)
            srl.is_valid(raise_exception=True)
            attrs['filter'] = srl.validated_data
        return attrs

    def create(self, validated_data, *args, **kwargs):
        return models.ActiveSearch.objects.create(
        user=self.context.get('user'),
        name=validated_data.get('name'),
        type=validated_data.get('type'),
        filter=validated_data.get('filter'),
        raw_filter=validated_data.get('raw_filter'),
        expire_time=timezone.now() + timezone.timedelta(days=validated_data.get('days'))
        )


class ActiveHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ActiveSearchHistory
        fields = (
        'name',
        'type',
        'raw_filter',
        'create_time',
        'expire_time',
         )

