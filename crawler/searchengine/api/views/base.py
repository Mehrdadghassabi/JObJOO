from itertools import chain
from multiprocessing.dummy import active_children
from urllib import response

from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from api import models
from api import tasks
from api.services import recruiment_services
from api.utils import Request


class SimilarAd(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, type, id):
        if type == 'recruiment':
            obj = models.RecruimentAds.get_by_id(id)
            if obj is not None:
                return Response(
                serializers.RecruimentAdWithSimilar(
                    obj,
                context={'request': request}
                ).data
                )
            return Response(
            {
                'message': 'Invalid ID'
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
        {
        'message': 'Invalid Type'
        },
        status=status.HTTP_400_BAD_REQUEST
        )


class DataRanges(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        try:
            recruiment_ranges = models.RecruimentAds.get_ranges()
            # home_appliance_ranges = models.HomeApplianceAds.get_ranges()
            # electronics_ranges = models.ElectronicsAds.get_ranges()
            # business_ranges = models.BusinessAds.get_ranges()
            # personal_stuff_ranges = models.PersonalStuffAds.get_ranges()
            province = models.Province.get_all()
            serialized_province = serializers.ProvinceSerializer(province, many=True).data
            return Response(
            {
            'homes': recruiment_ranges,
            'provinces': serialized_province
            },
            status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
            {
            'message': 'unexpected error {}'.format(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class Province(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        data = serializers.ProvinceSerializer(models.Province.get_all(), many=True).data
        return Response(
        {
        'provinces': data
        },
        status=status.HTTP_200_OK
        )


class City(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, id):
        data = serializers.CitySerializer(models.City.get_cities(id), many=True).data
        return Response(
        {
        'cities': data
        },
        status=status.HTTP_200_OK
        )


class Favourite(APIView):
    serializer_class = serializers.SaveFavourite

    def get(self, request):
        try:
            typ = request.query_params.get('type')
            page = int(request.query_params.get('page', 1))
            user = request.user.id
            message, state = tasks.recruiment_service.delay('get_favorites', typ, page, user).get()
            return Response(
             message
            ,
            status=state
            )
        except Exception as e:
            return Response(
            {
            'message': 'Internal Server Error' + str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            data = request.data
            user = request.user.id
            message, state = tasks.recruiment_service.delay('save_favorite', data, user).get()
            return Response(
            message,
            status=state
            )
        except Exception as e:
            return Response(
            {
            'message': 'Internal Server Error' + str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request):
        try:
            typ = typ = request.query_params.get('type')
            token = int(request.query_params.get('token'))
            user = request.user.id
            message, state = tasks.recruiment_service.delay('delete_favorite', typ, token, user).get()
            return Response(
                message,
                status=state
            )
        except Exception as e:
            return Response(
            {
            'message': 'Internal Server Error' + str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ApplicationsMainPage(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        recruiment_sources = models.RecruimentAds.objects.all().distinct('source').values_list('source')
        
        recruiments = []
        homes = []

        for i in recruiment_sources:
            recruiments.append(
            {
            "source": serializers.SourceSerializer(
            models.Source.objects.get(id=i[0])
            ).data,
            "data": serializers.CarSerializer(
            models.CarAds.objects.filter(
            source=i[0]
            ).order_by('-time')[:10],
            many=True,
            context={'request': request}
            ).data
            }
            )
        
    
        return Response(
        {
        'recruiment': recruiments,

        },
        status=status.HTTP_200_OK
        )


class NotificationToken(APIView):

    def post(self, request):
        serializer = serializers.NotificationToken(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
            {
            'message': 'Token stored',
            },
            status=status.HTTP_200_OK
            )
        return Response(
        {
        'message': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
        )


class Banner(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response(
        serializers.Banner(
        models.Banner.objects.all(),
        many=True,
        context={'request': request}
        ).data
        )


class GetAd(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, type, id):
        try:
            if type == 'recruiment':
                return Response(
                    serializers.RecruimentSerializer(
                        models.RecruimentAds.objects.get(token=id),
                        context={'request': request}
                ).data
                )
            raise Exception
        except Exception as e:
            return Response(
            {
            'message': 'Invalid type or id' + str(type) + '\n' +str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
            )
