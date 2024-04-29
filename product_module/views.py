from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Product, ProductCategory, ProductBrand
from django.http import Http404
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, View, DetailView
from django.http import HttpRequest
from sitesettings_module.models import SiteBanner
from utils.http_service import get_client_ip
from utils.convertors import group_list
from .models import ProductVisit, ProductGallery

# Create your views here.


# def product_list(request):

#     products = Product.objects.all().order_by('price')

#     context = {
#         'products':products
#     }
#     return render(request, 'product_module/product_list.html', context)

class ProductListView(ListView):
    
    # template_name = 'product_module/product_list.html'
    # model = Product
    # context_object_name = 'products'

    # def get_queryset(self):
    #     base_query = super(ProductListView, self).get_queryset()
    #     data = base_query.filter(is_active=True)
    #     return data


    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 7

    # def get_context_data(self, **kwargs):
    #     context = super(ProductListView, self).get_context_data()
    #     query = Product.objects.all()
    #     product: Product = query.order_by('-price').first()
    #     db_max_price = product.price if product is not None else 0
    #     context['db_max_price'] = db_max_price

    #     context['start_price'] = self.request.GET.get('start_price') or 0
    #     context['end_price'] = self.request.GET.get('end_price') or db_max_price

    #     return context

    def get_context_data(self, *, object_list=None, **kwargs):
        print('context_data')
        context = super(ProductListView, self).get_context_data()
        query = Product.objects.all()
        product: Product = query.order_by('-price').first()
        db_max_price = product.price if product is not None else 0
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = SiteBanner.objects.filter(is_active=True, position__iexact=SiteBanner.SiteBannerPositions.product_list)
        return context

    def get_queryset(self):
        Query = super(ProductListView, self).get_queryset()
        data = Query.filter(is_active=True)
        return data
    
    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request: HttpRequest = self.request
        print(request.GET)

        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')

        if start_price is not None:
            query = query.filter(price__gte=start_price)

        if end_price is not None:
            query = query.filter(price__lte=end_price)



        if brand_name is not None:
            query = query.filter(Brand__url_title__iexact=brand_name)


        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
            
        return query






# def product_detail(request, slug):

#     products = get_object_or_404(Product, slug=slug)
#     context = {
#         'product':products
#     }
#     return render(request, 'product_module/product_detail.html', context)


class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product

    
    



    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        # what is the loaded_product? it is the product that got fetched from the model Product
        loaded_product = self.object
        request = self.request
        favorite_product_id = request.session.get("product_favorites")
        context['is_favorite'] = favorite_product_id == str(loaded_product.id)

        context['product_galleries'] = group_list(list(ProductGallery.objects.filter(product_id=loaded_product.id).all()), 3)
        
        context['related_products'] = group_list(list(Product.objects.filter(Brand_id=loaded_product.Brand_id).exclude(pk=loaded_product.id).all()[:12]), 3)


        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id

        has_ben_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()

        if not has_ben_visited:
            new_visit = ProductVisit(user_id=user_id, ip=user_ip, product_id=loaded_product.id)
            new_visit.save()

        return context
    


class AddProductFavorite(View):
    def post(self, request):
        product_id = request.POST["product_id"]
        product = Product.objects.get(pk=product_id)
        request.session["product_favourite"] = product_id
        return redirect(product.get_absolute_url())




# def product_categories_component(request):
#     categories = ProductCategory.objects.filter(is_active=True, is_delete=False)
#     context = {
#         'categories':categories
#     }
#     return render(request, 'components/product_categories.html', context)


def product_categories_component(request: HttpRequest):
    product_categories = ProductCategory.objects.filter(is_active=True, is_delete=False)
    context = {
        'categories': product_categories
    }
    return render(request, 'components/product_categories.html', context)




def product_brands_component(request:HttpRequest):
    product_brands = ProductBrand.objects.annotate(products_count=Count('product')).filter(is_active=True)
    context = {
        'brands':product_brands
    }
    return render(request, 'components/product_brands.html', context)
    


    









