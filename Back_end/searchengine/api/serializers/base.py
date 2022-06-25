import collections

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api import models


class NotificationToken(serializers.ModelSerializer):
    device = serializers.CharField(source='device.name')

    class Meta:
        model = models.NotificationsToken
        fields = (
        'token',
        'device'
        )

    def validate_device(self, attrs):
        try:
            models.DeviceType.objects.get(name=attrs)
            return attrs
        except models.DeviceType.DoesNotExist:
            raise ValidationError(
                'Acceptable device name are: {}'.format(
                [i['name'] for i in models.DeviceType.objects.values('name')]
                )
                )

    def save(self, **kwargs):
        models.NotificationsToken.objects.update_or_create(
            user=kwargs['user'],
            device=models.DeviceType.objects.get(name=self.validated_data['device']['name']),
            defaults={'token': self.validated_data['token']}
            )


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Source
        fields = '__all__'


class RangeSerializer(serializers.Serializer):
    min = serializers.FloatField(required=False)
    max = serializers.FloatField(required=False)


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Province
        fields = (
            'id',
            'name'
            )


class CitySerializer(serializers.ModelSerializer):
 class Meta:
    model = models.City
    fields = (
        'id',
        'name'
        )


class Neighbourhood(serializers.Serializer):
    name = serializers.CharField(source='neighbourhood')


class Banner(serializers.ModelSerializer):
    class Meta:
       model = models.Banner
       fields = '__all__'


class SearchBaseSerializer(serializers.Serializer):

    def validate(self, attrs):
        attrs = super().validate(attrs)
        cleaned_data = {}
        for i, j in attrs.items():
            if j is not None:
                if not isinstance(j, collections.OrderedDict):
                    if isinstance(j, list):
                        cleaned_data['{}__in'.format(i)] = j
                    else:
                        cleaned_data[i] = j
                else:
                    if j.get('min', False):
                        cleaned_data['{}__gte'.format(i)] = j['min']
                    if j.get('max', False):
                        cleaned_data['{}__lte'.format(i)] = j['max']
        return cleaned_data


class SaveFavourite(serializers.ModelSerializer):
    class Meta:
        model = models.Favourite
        fields = (
        'type',
        'token',
        )

    def validate(self, attrs):
        attrs = super(SaveFavourite, self).validate(attrs)
        try:
            if attrs.get('type') == 'recruiment':
                models.RecruimentAds.objects.get(token=attrs.get('token'))
            models.Favourite.objects.get(
                user=self.context.get('user'),
                token=attrs.get('token'),
                type=attrs.get('type')
                )
            raise serializers.ValidationError('This item is in your favourites')
        except models.RecruimentAds.DoesNotExist:
            raise serializers.ValidationError('Invalid token')
        except models.Favourite.DoesNotExist:
            return attrs


class ResultSearchBaseSerializer(serializers.ModelSerializer):
    favourite = serializers.SerializerMethodField()
    source = SourceSerializer()

    def get_favourite(self, obj):
        request = self.context.get('request', False)
        if request and request.user.is_authenticated:
            try:
                models.Favourite.objects.get(user=request.user, token=obj.token)
                return True
            except models.Favourite.DoesNotExist:
                return False
        return None