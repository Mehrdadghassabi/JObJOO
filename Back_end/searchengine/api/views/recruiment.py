import traceback

from django.core.paginator import Paginator
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from django.db.models import F

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from api import serializers
from api import models


class SearchRecruiment(APIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.SearchRecruimentSerializer

    def get_serializer(self):
        return serializers.SearchRecruimentSerializer()

    def post(self, request, page):
        serializer = serializers.SearchRecruimentSerializer(data=request.data)
        if serializer.is_valid():
            data = models.RecruimentAds.search(**serializer.validated_data)
            paginator = Paginator(data, 12)
            try:
                result = serializers.ResultSearchRecruimentSerializer(paginator.page(page), many=True,
                context={'request': request})
            except:
                result = serializers.ResultSearchRecruimentSerializer(paginator.page(1), many=True,
                context={'request': request})
            return Response(
            {
            'page_counts': paginator.num_pages,
            'counts': paginator.count,
            'current_page': page,
            'result': result.data
            },
            status=status.HTTP_200_OK
            )
        return Response(
        {
        'message': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, page):
        serializer = serializers.SearchRecruimentSerializer(data=request.data)
        if serializer.is_valid():
            data = models.RecruimentAds.search(**serializer.validated_data)
            paginator = Paginator(data, 12)
            try:
                result = serializers.ResultSearchRecruimentSerializer(paginator.page(page), many=True,
                context={'request': request})
            except:
                result = serializers.ResultSearchRecruimentSerializer(paginator.page(1), many=True,
                context={'request': request})
            return Response(
            {
            'page_counts': paginator.num_pages,
            'counts': paginator.count,
            'current_page': page,
            'result': result.data
            },
            status=status.HTTP_200_OK
            )
        return Response(
        {
        'message': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
        )


class MainPageRecruiment(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, page):
        try:
            recruiment = models.RecruimentAds.objects.raw(
            '''select * from 
            (
            (select *, row_number() over (order by time desc) r from recruiment where source_id=1 limit 5 offset {}) union 
            (select *, row_number() over (order by time desc) r from recruiment where source_id=2 limit 5 offset {})
            ) as x order by r;'''.format(
            5 * (page - 1),
            5 * (page - 1),
            )
            )
            count = models.RecruimentAds.objects.all().count()
            
            result = serializers.ResultSearchRecruimentSerializer(
            recruiment,
            many=True,
            context={'request': request}
            )
            return Response(
            {
            'page_counts': count // 10,
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