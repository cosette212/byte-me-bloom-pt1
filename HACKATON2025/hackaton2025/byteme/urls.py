from . import views
from django.urls import path

urlpatterns = [
    path('', views.index_view, name='index'),
    path('result/', views.result_view, name='result')
]
