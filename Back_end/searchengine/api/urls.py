from django.urls import path
from django.views.decorators.cache import cache_page

from api.views import *


urlpatterns = [
    path('active/search/', ActiveSearch.as_view(), name='active_search'),
    path('active/search/<int:id>/', ActiveSearch.as_view(), name='delete_active_search'),
    path('active/search/history/', ActiveSearchHistory.as_view(), name='active_search_history'),
    path('active/search/result/<str:typ>/<int:id>/<int:fTime>/<int:tTime>/<int:page>/', ActiveSearchResult.as_view(),
            name='active_search_result'),
    path('search/recruiment/<int:page>/', SearchRecruiment.as_view(), name='search_recruiment'),
    path('data/ranges/', cache_page(60 * 60 * 24 * 7)(DataRanges.as_view()), name='data_ranges'),
    path('province/', Province.as_view(), name='province'),
    path('city/<int:id>/', City.as_view(), name='city'),
    path('recruiment/main/page/<int:page>/', MainPageRecruiment.as_view(), name='recruiment_main_page'),
    path('favourite/', Favourite.as_view(), name='favourite'),
    path('notification/', NotificationToken.as_view(), name='notification'),
    path('similar/ads/<str:type>/<str:id>/', SimilarAd.as_view(), name='ad'),
    path('banner/', Banner.as_view(), name='banner'),
    path('ad/<str:type>/<str:id>/', GetAd.as_view(), name='get_ad'),
]