from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Article, ArticleCategory, ArticleComment
from django.views import View
from django.views.generic import ListView, DetailView
from jalali_date import datetime2jalali, date2jalali
# Create your views here.
from django.http import HttpRequest, HttpResponse
# from django.contrib.auth.decorators import login_required


# class ArticleView(View):
#     def get(self, request):
#         articles = Article.objects.filter(is_active=True)
#         context = {
#             'articles':articles
#         }
#         return render(request, 'Article.html', context)


class ArticleListView(ListView):
    model = Article
    template_name  = 'Article.html'
    paginate_by = 5

    
    def get_context_data(self, *args, **kwargs ):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        # context['date'] =  date2jalali(self.request.user.date_joined)

        return context
    
    def get_queryset(self):
        query = super(ArticleListView, self).get_queryset()
        query = query.filter(is_active=True)
        
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(selected_categories__url_title__iexact=category_name)

        return query

    
    
 
    



def article_categories_components(request:HttpRequest):
    article_main_categories = ArticleCategory.objects.prefetch_related('articlecategory_set').filter(is_active=True, parent_id=None)

    context = {
        'main_categories':article_main_categories
    }

    return render(request, 'components/article_category_components.html', context)



# class ArticleDetailView(DetailView):
#     model = Article
#     template_name = 'Article_Detail.html'

#     def get_queryset(self):
#         query = super(ArticleDetailView, self).get_queryset()
#         query = query.filter(is_active=True)
#         return query
    
    
#     def get_context_data(self, **kwargs):
#         context = super(ArticleDetailView, self).get_context_data()
#         article: Article = kwargs.get('object')
#         context['comments'] = ArticleComment.objects.filter(article_id=article.id, parent=None).order_by('-create_date').prefetch_related('articlecomment_set'),
#         context['comments_count'] = ArticleComment.objects.filter(article_id=article.id).count()

#           #we set the .order_by which means it will return the newest comment
#         return context
        


# def add_article_comment(request: HttpResponse):
#     if request.user.is_authenticated:
#         article_id = request.GET.get('article_id')
#         article_comment = request.GET.get('article_comment')
#         parent_id = request.GET.get('parent_id')
#         new_comment = ArticleComment(article_id=article_id, text=article_comment, user_id=request.user.id, parent_id=parent_id)
#         print(new_comment)
#         new_comment.save()

#         context = {
#             'comments': ArticleComment.objects.filter(article_id=article_id, parent=None).order_by('-create_date').prefetch_related('articlecomment_set'),
#             'comments_count': ArticleComment.objects.filter(article_id=article_id).count()
#         }

#         return render(request, 'Includes/articles_comments_partial.html', context)
        
#     return HttpResponse('response')
        


    
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'Article_Detail.html'

    def get_queryset(self):
        query = super(ArticleDetailView, self).get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        article: Article = kwargs.get('object')
        context['comments'] = ArticleComment.objects.filter(article_id=article.id, parent=None).order_by('-create_date').prefetch_related('articlecomment_set')
        context['comments_count'] = ArticleComment.objects.filter(article_id=article.id).count()
        return context


def article_categories_component(request: HttpRequest):
    article_main_categories = ArticleCategory.objects.filter(is_active=True, parent_id=None)

    context = {
        'main_categories': article_main_categories
    }
    return render(request, 'components/article_category_components.html', context)


def add_article_comment(request: HttpRequest):
    if request.user.is_authenticated:
        article_id = request.GET.get('article_id')
        article_comment = request.GET.get('article_comment')
        parent_id = request.GET.get('parent_id')
        print(article_id, article_comment, parent_id)
        new_comment = ArticleComment(article_id=article_id, text=article_comment, user_id=request.user.id, parent_id=parent_id)
        new_comment.save()
        context = {
            'comments': ArticleComment.objects.filter(article_id=article_id, parent=None).order_by('-create_date').prefetch_related('articlecomment_set'),
            'comments_count': ArticleComment.objects.filter(article_id=article_id).count()
        }

        return render(request, 'Includes/articles_comments_partial.html', context)

    return HttpResponse('response')