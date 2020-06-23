from django.urls import path, include
from .views import CostService

urlpatterns = [
    path('<int:pk>/', CostService.as_view()),
    path('', CostService.as_view()),
]

