from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('records', views.fetch_records, name='fetch-records'),
    path('download', views.download_file)
]
