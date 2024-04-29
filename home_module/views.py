from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView
from sitesettings_module.models import SiteSettings, Slider
from product_module.models import Product, ProductCategory
from utils.convertors import group_list
from utils.http_service import get_client_ip
from django.db.models import Count
from django.db.models import Sum 
# Create your views here.

def index_page(request):
    return render(request, 'home_module/Home_page.html')

class HomeView(TemplateView):
    template_name = 'home_module/Home_page.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         sliders = Slider.objects.filter(is_active=True)
#         context['sliders'] = sliders
#         #this code below will return the latest 12 products that we added in the admin panel
#         # latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:12]
#         # context['latest_products'] = group_list(latest_products)
#         latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:12]
#         context['latest_products'] = group_list(latest_products)

#         return context
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sliders = Slider.objects.filter(is_active=True)
        context['sliders'] = sliders
        latest_products = Product.objects.filter(is_active=True).order_by('-id')[:12]
        most_visited_products = Product.objects.filter(is_active=True).annotate(visit_count=Count('productvisit')).order_by('-visit_count')[:12]

        context['latest_products'] = group_list(latest_products)
        context['most_visited_products'] = group_list(most_visited_products)
        
        categories = list(ProductCategory.objects.filter(is_active=True)[:6])
        categories_product = []
        
        for category in categories:
            item = {
                'id':category.id,
                'title':category.title,
                'products': list(category.categories_products.all()[:4  ])
            }
            categories_product.append(item)
        
        print(category.categories_products.all())

        context['categories_products'] = categories_product


        most_bought_products = Product.objects.filter(orderdetail__order__is_paid=True).annotate(order_count=Sum(
            'orderdetail__count'
        )).order_by('-order_count')[:12]

        context['most_bought_products'] = group_list(most_bought_products)
    
        

        return context



def render_partial_header(request):

    settings: SiteSettings = SiteSettings.objects.filter(is_main_setting=True).first()

    context = {
        'settings':settings
    }

    return render(request, 'Shared/Header_render_partial.html', context)



def render_partial_footer(request):
    settings: SiteSettings = SiteSettings.objects.filter(is_main_setting=True).first()

    context = {
        'settings':settings
    }

    return render(request, 'Shared/Footer_render_partial.html', context)



class About_us(TemplateView):
    template_name = 'About_us.html'

    def get_context_data(self, **kwargs):

        settings: SiteSettings = SiteSettings.objects.filter(is_main_setting=True).first()

        context = super().get_context_data(**kwargs)

        context['about'] = settings

        return context


