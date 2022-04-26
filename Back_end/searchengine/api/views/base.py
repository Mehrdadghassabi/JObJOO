from itertools import chain

from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from api import models


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
            if typ:
                if typ in [i[0] for i in models.active_search.TYPES]:
                    favourites = models.Favourite.objects.filter(user=request.user, type=typ).order_by('-time')
                    paginator = Paginator(favourites, 12)
                    try:
                        result = paginator.page(page)
                    except:
                        result = paginator.page(1)
                        page = 1
                    ids = [i.token for i in result]
                    if typ == 'recruiment':
                        data = serializers.FavouriteResultRecruiment(
                        models.RecruimentAds.objects.filter(token__in=ids),
                        many=True
                        ).data
                    else:
                        return Response(
                        {
                        'message': 'Invalid type'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                        )
            else:
                favourites = models.Favourite.objects.filter(user=request.user).order_by('-time')
                paginator = Paginator(favourites, 12)
                try:
                    result = paginator.page(page)
                except:
                    result = paginator.page(1)
                    page = 1
                data = []
                for i in result:
                    if i.type == 'recruiment':
                        try:
                            data.append(
                            serializers.FavouriteResultRecruiment(
                            models.RecruimentAds.objects.get(token=i.token)
                            ).data
                            )
                        except models.RecruimentAds.DoesNotExist:
                            i.delete()
                return Response(
                {
                'page': page,
                'pages': paginator.num_pages,
                'data': data
                }
                )
        except Exception as e:
            return Response(
            {
                'message': 'Unexpected error, try again later',
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        serializer = serializers.SaveFavourite(data=request.data, context={'request': request})
        if serializer.is_valid():
            if serializer.save(user=request.user) is not None:
                return Response(
                {
                'message': 'Favourite saved successfully!'
                },
                status=status.HTTP_200_OK
                )
            return Response(
            {
            'message': 'Ad is in your favourite or invalid ID'
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
        {
        'message': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request):
        try:
            typ = request.query_params.get('type')
            token = int(request.query_params.get('token'))
            models.Favourite.objects.get(user=request.user, type=typ, token=token).delete()
            return Response(
                    {
                        'message': 'Favourite deleted successfully!'
                    }, status=status.HTTP_200_OK
                    )
        except:
            return Response(
            {
            'message': 'Invalid data!'
            },
            status=status.HTTP_400_BAD_REQUEST
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
                serializers.ResultSearchRecruimentSerializer(
                models.RecruimentAds.objects.get(token=id),
                context={'request': request}
                )
                )
            raise Exception
        except Exception as e:
            return Response(
            {
            'message': 'Invalid type or id'
            },
            status=status.HTTP_400_BAD_REQUEST
            )
