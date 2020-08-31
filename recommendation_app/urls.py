from django.urls import path

from recommendation_app import views


urlpatterns = [
    path('recommendations', views.get_recommendations, name='list-recommendations'),
]
