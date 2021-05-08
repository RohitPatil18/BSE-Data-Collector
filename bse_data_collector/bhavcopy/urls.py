from django.urls import path

from .views import index, fetch_records

urlpatterns = [
    path('', index, name='index'),
    path('records', fetch_records, name='fetch-records')
]
