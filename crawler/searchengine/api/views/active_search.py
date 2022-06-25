from itertools import chain

from django.core.paginator import Paginator
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api import serializers
from api import models


class ActiveSearch(APIView):
    serializer_class = serializers.SetActiveSearchSerializer

    def get(self, request):
        serializer = serializers.GetActiveSearchSerializer(
        models.ActiveSearch.get_user_searches(request.user),
        many=True
         )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.SetActiveSearchSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            if request.user.profile.has_credit():
                request.user.profile.pay(serializer.validated_data.get('days'))
                serializer.validated_data['raw_filter'] = request.data['filter']
                serializer.save(
                user=request.user,
                    )
                return Response(
                {'message': 'active search created'},
                status=status.HTTP_200_OK
                )
            return Response(
            {'message': 'you have no enough credit'},
            status=status.HTTP_402_PAYMENT_REQUIRED
            )
        return Response(
        {'message': serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request, id):
       active_search = models.ActiveSearch.is_owner(request.user, id)
       if active_search:
           serializer = serializers.SetActiveSearchSerializer(data=request.data, context={'user': request.user})
           if serializer.is_valid():
               models.ActiveSearchHistory.objects.create(
               user=active_search.user,
               filter=active_search.filter,
               raw_filter=active_search.raw_filter,
               create_time=active_search.create_time,
               expire_time=timezone.now()
               )
               serializer.validated_data['raw_filter'] = request.data['filter']
               serializer.update(
               active_search,
               serializer.validated_data,
               )
               return Response(
               {'message': 'active search updated'},
               status=status.HTTP_200_OK
               )
           return Response(
           {'message': serializer.errors},
           status=status.HTTP_400_BAD_REQUEST
           )
       return Response(
       {'message': 'there are not active search with this id'},
       status=status.HTTP_400_BAD_REQUEST
       )

    def delete(self, request, id):
        active_search = models.ActiveSearch.is_owner(request.user, id)
        if active_search:
            models.ActiveSearchHistory.objects.create(
            user=active_search.user,
            filter=active_search.filter,
            raw_filter=active_search.raw_filter,
            create_time=active_search.create_time,
            expire_time=active_search.expire_time
            )
            active_search.delete()
            return Response(
            {'message': 'active search deleted'},
            status=status.HTTP_200_OK
            )
        return Response(
        {'message': 'there are not active search with this id'},
        status=status.HTTP_400_BAD_REQUEST
        )


class ActiveSearchHistory(APIView):

    def get(self, request):
        serializer = serializers.ActiveHistorySerializer(
            sorted(
            list(
                chain(
                    models.ActiveSearchHistory.get_user_searches(request.user),
                    models.ActiveSearch.get_user_expired_searches(request.user)
                 )
                ),
                key=lambda i: i.create_time,
                reverse=True
                ),
                many=True
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ActiveSearchResult(APIView):

    def get(self, request, typ, id, fTime, tTime, page):
        def paging(data, serializer):
            paginator = Paginator(data, 12)
            try:
                result = serializer(
                paginator.page(page),
                many=True,
                context={'request': request}
                )
            except:
                result = serializer(
                paginator.page(1),
                many=True,
                context={'request': request}
                )
            return paginator, result

        try:
            active_search = models.ActiveSearch.objects.get(id=id, user=request.user)
            fltr = active_search.filter
            fltr['time'] = fTime
            fltr['time__lte'] = tTime
            if active_search.type == 'recruiment':
                data = models.RecruimentAds.search(**fltr)
                paginator, result = paging(data, serializers.ResultSearchRecruimentSerializer)
            return Response(
                {
                'page_counts': paginator.num_pages,
                'counts': paginator.count,
                'current_page': page,
                'result': result.data
                },
                status=status.HTTP_200_OK
                )
        except models.ActiveSearch.DoesNotExist:
            return Response(
            {
            'message': 'Invalid ID'
            },
            status=status.HTTP_400_BAD_REQUEST
            )