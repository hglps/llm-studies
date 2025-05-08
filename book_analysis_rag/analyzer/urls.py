from django.urls import path
from .views import upload_article, article_list, article_detail, home
from django.contrib import admin


urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_article, name='upload_article'),
    path('articles/', article_list, name='article_list'),
    path('articles/<int:article_id>/', article_detail, name='article_detail'),
]