from django.shortcuts import render, redirect
from django.urls import reverse
from article_module.models import Article
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

# Create your views here.

def permission_checker_decorator_factory(data):

    def permission_checker_decorator(func):

        def wrapper(request, *args, **kwargs):
            print(data)
            if request.user.is_authenticated and request.user.is_superuser:
                return func(request, *args, **kwargs)
            else:
                return redirect(reverse('login_page'))
        
        return wrapper
    return permission_checker_decorator

@permission_checker_decorator_factory('This is my data for main admin page')
def Index(request):
    return render(request, 'home/index.html')


@method_decorator(permission_checker_decorator_factory('this is my data for article page'), name='dispatch')
class ArticleListView(ListView):
    model = Article
    template_name  = 'articles/articles_list.html'
    paginate_by = 5

    
    def get_context_data(self, *args, **kwargs ):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        # context['date'] =  date2jalali(self.request.user.date_joined)

        return context
    
    def get_queryset(self):
        query = super(ArticleListView, self).get_queryset()
        query = query.all()
        
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(selected_categories__url_title__iexact=category_name)

        return query



class ArticleEditView(UpdateView):
    model = Article
    template_name = 'articles/edit_article.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_articles')