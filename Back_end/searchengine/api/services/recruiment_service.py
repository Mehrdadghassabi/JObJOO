import traceback

from django.core.paginator import Paginator
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from django.contrib.auth.models import User as djUser
from django.db.models import F
from django.core.cache import cache

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from api import serializers
from api import models


class recruiment_services():
    def get_main_page(self, request, page):
        try:
            recruiment = models.RecruimentAds.objects.raw(
            '''select * from 
            (
            (select *, row_number() over (order by time desc) r from recruiment where source_id=1 limit 6 offset {}) union 
            (select *, row_number() over (order by time desc) r from recruiment where source_id=2 limit 6 offset {})
            ) as x order by r;'''.format(
            6 * (page - 1),
            6 * (page - 1),
            )
            )
            count = cache.get('recruiment_counts')

            if count is None:
                count = models.RecruimentAds.objects.all().count()
                cache.set('recruiment_counts', count, timeout=60 * 60 * 24 * 1)
            
            result = serializers.ResultSearchRecruimentSerializer(
            recruiment,
            many=True,
            context={'request': request}
            )
            return Response(
            {
            'page_counts': count // 12,
            'counts': count,
            'current_page': page,
            'result': result.data
            },
            status=status.HTTP_200_OK
            )
        except:
            traceback.print_exc()
            return Response(
            {
            'message': 'Internal error'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_favorites(self, typ, page, user):
        try:
            user = djUser.objects.get(id=user)
            if typ:
                if typ in [i[0] for i in models.active_search.TYPES]:
                    favourites = models.Favourite.objects.filter(user=user, type=typ).order_by('-time')
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
                        return ({'message': 'Invalid type'}, status.HTTP_400_BAD_REQUEST)
            else:
                favourites = models.Favourite.objects.filter(user=user).order_by('-time')
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
                return ({
                'page': page,
                'pages': paginator.num_pages,
                'data': data
                },
                status.HTTP_200_OK)
        except Exception as e:
            return({
                'message': 'Unexpected error, try again later',
            },
            status.HTTP_500_INTERNAL_SERVER_ERROR)


    def save_favorite(self, data, user):
        user = djUser.objects.get(id=user)
        serializer = serializers.SaveFavourite(data=data, context={'user': user})
        if serializer.is_valid():
            if serializer.save(user=user) is not None:
                return ({'message':'Favourite saved successfully!'}, status.HTTP_200_OK)
            return ({'message': 'Ad is in your favourite or invalid ID'}, status.HTTP_400_BAD_REQUEST)
        return ({'message': serializer.errors}, status.HTTP_400_BAD_REQUEST)

    def delete_favorite(self, typ, token, user):
        try:
            user = djUser.objects.get(id=user)
            models.Favourite.objects.get(user=user, type=typ, token=token).delete()
            return ({'message':'Favourite deleted successfully!'}, status.HTTP_200_OK)
        except Exception as e:
            return ({'message':'Invalid data'}, status.HTTP_400_BAD_REQUEST)