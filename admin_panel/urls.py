from django.urls import path
from .views import ArticleListView, ArticleEditView, Index

urlpatterns = [
    path('', Index, name='admin_dashboard'),
    path('articles/', ArticleListView.as_view(), name='admin_articles'),
    path('articles/edit/<pk>', ArticleEditView.as_view(), name='article_edit')
]


