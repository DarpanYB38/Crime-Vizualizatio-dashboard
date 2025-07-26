from django.urls import path
from Crimes.views import *

urlpatterns = [
    path('',home,name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('crime/<int:crime_id>/', detail, name='details'),
    path("similarity-search/", similarity_search, name="similarity_search"),
    path("crime-trends/", crime_trends, name="crime_trends"),
    path("crime-map/", crime_hotspot_map, name="crime_map"),
    path('heatmap/', heatmap_view, name='heatmap'),
    path('predict-crime/', predict_crime_view, name='predict_crime'),
]
