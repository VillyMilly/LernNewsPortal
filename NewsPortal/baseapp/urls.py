from .views import NewsList, NewsDetail
from django.urls import path

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view()),
]