from django.urls import path
from .views import ArticleListView, ArticleDetailView, add_article_comment
urlpatterns = [
    path('', ArticleListView.as_view(), name='article_page'),
    path('cat/<str:category>', ArticleListView.as_view(), name='article_by_category_list'),
    path('<pk>/', ArticleDetailView.as_view(), name='article_detail' ),
    path('add-article-comment', add_article_comment, name='add_article')
]