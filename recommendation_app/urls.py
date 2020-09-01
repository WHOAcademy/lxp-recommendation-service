from django.urls import path

from recommendation_app import views


urlpatterns = [
    path('recommendations/<str:keycloak_id>', views.RecommendationListView.as_view(), name='list-recommendations'),
]
