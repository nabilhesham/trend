from django.urls import path, include
from .views import home, search_results

urlpatterns = [
    path('', home, name="home"),
    path('search_results/<str:trend_name1>-<str:trend_name2>-<str:search_type>/', search_results, name="search_results")
]