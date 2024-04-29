from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404
from django.views.generic import TemplateView, View, ListView
from .forms import EditProfileModelForm, ChangePasswordForm
from account_module.models import User
from django.contrib.auth import logout
from django.urls import reverse
from order_module.models import Order, OrderDetail, Product
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

# @method_decorator(login_required, name='dispatch')
class UserPanelView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = 'UserPanel.html'




@method_decorator(login_required, name='dispatch')
class UsersProducts(ListView):
    model = Order
    template_name = 'user_bought_products.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request
        queryset = queryset.filter(user_id=request.user.id, is_paid=True)

        return queryset



def my_shopping_detail(request: HttpRequest, order_id):
    order = Order.objects.prefetch_related('orderdetail_set').filter(pk=order_id, user_id=request.user.id).first()
    if order is None:
        raise Http404('سبد خرید مورد نظر یافت نشد')

    return render(request, 'user_bought_products.html', {
        'order': order
    })


@method_decorator(login_required, name='dispatch')
class EditUserProfileView(View):
    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(instance=current_user)

        context = {
            'form':edit_form,
            'current_user':current_user,
        }
        return render(request, 'EditProfile.html', context)
    
    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)

        context = {
            'form':edit_form,
            'current_user':current_user,
        }
        return render(request, 'EditProfile.html', context)


class ChangePasswordView(View):
    def get(self, request):
        
        context = {
            'password_form':ChangePasswordForm(),
            'current_user':User
        }
        return render(request, 'ChangePassword.html', context)
    
    def post(self, request):
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            current_user: User = User.objects.filter(id=request.user.id).first()
               #this gets the password and compares the password with the current password 
            if current_user.check_password(form.cleaned_data.get('current_password')):
                     #this will set the a new password witht what the user has assigned
                     # on the new_password form
                current_user.set_password(form.cleaned_data.get('new_password'))
                current_user.save()
                logout(request)
                return redirect('/login')
            else:
                form.add_error('new_password', 'رمز عبور اشتباه است')
                

        context = {
            'password_form':form
        }
        return render(request, 'ChangePassword.html', context)
    

@login_required
def user_panel_menu_component(request: HttpRequest):

    return render(request, 'components/user_panel_menu.html')



@login_required
def user_basket(request):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False, user_id=request.user.id)
    total_ammout = 0

    for order_detail in current_order.orderdetail_set.all():
        total_ammout += order_detail.product.price * order_detail.count  

    context = {
        'order':current_order,
        'sum':total_ammout,
    } 


    return render(request, 'User_Basket.html', context)









def remove_order_detail(request):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'not_found_detail_id'
        })

    deleted_count, deleted_dict = OrderDetail.objects.filter(id=detail_id, order__is_paid=False, order__user_id=request.user.id).delete()

    if deleted_count == 0:
        return JsonResponse({
            'status': 'detail_not_found'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False, user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount
    }
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('User_Basket_Content.html', context)
    })


# def change_count_products(request):
#     detail_id = request.GET.get('detail_id')
#     state = request.GET.get('state')
#     if detail_id is None and state is None:
#         return JsonResponse({
#             'status': 'not_found_detail_id_state'
#         })
    
#     order_detail = OrderDetail.objects.filter(order__is_paid=False, id=detail_id, order__user_id=request.user.id).first()


#     if order_detail is None:
#         return JsonResponse({
#             'status':'detail_not_found'
#         })

#     if state == 'increase':
#         order_detail.count += 1
#         order_detail.save()
#     elif state == 'decrease':
#         if order_detail.count == 1:
#             order_detail.delete()
#         else:
#             order_detail.count -= 1
#             order_detail.save()
#     else:
#         return JsonResponse({
#             'status':'invalid_state_count'
#         })    


#     current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False, user_id=request.user.id)
#     total_amount = current_order.calculate_total_price()

#     context = {
#         'order': current_order,
#         'sum': total_amount
#     }
#     return JsonResponse({
#         'status': 'success',
#         'body': render_to_string('User_Basket_Content.html', context)
#     })


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def change_order_detail_count(request: HttpRequest):
    if request.method == 'POST':
        detail_id = request.GET.get('detail_id')
        state = request.GET.get('state')
        if detail_id is None or state is None:
            return JsonResponse({
                'status': 'not_found_detail_or_state'
            })

        order_detail = OrderDetail.objects.filter(id=detail_id, order__user_id=request.user.id, order__is_paid=False).first()

        if order_detail is None:
            return JsonResponse({
                'status': 'detail_not_found'
            })

        if state == 'increase':
            order_detail.count += 1
            order_detail.save()
        elif state == 'decrease':
            if order_detail.count == 1:
                order_detail.delete()
            else:
                order_detail.count -= 1
                order_detail.save()
        else:
            return JsonResponse({
                'status': 'state_invalid'
            })

        current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False, user_id=request.user.id)
        total_amount = current_order.calculate_total_price()

        context = {
            'order': current_order,
            'sum': total_amount
        }
        return JsonResponse({
            'status': 'success',
            'body': render_to_string('User_Basket_Content.html', context)
        })









# <div id="order-detail-content">

# <section id="cart_items">
#     <div class="container">
#         <div class="breadcrumbs">
#             <ol class="breadcrumb">
#               <li><a href="#">خانـه</a></li>
#               <li class="active">پرداخت</li>
#             </ol>
#         </div><!--/breadcrums-->
#         <div class="table-responsive cart_info">
#             <table class="table table-condensed">
#                 <thead>
#                     <tr class="cart_menu">
#                         <td class="image">کـالا</td>
#                         <td class="description"></td>
#                         <td class="price">قیمت</td>
#                         <td class="quantity">تعـداد</td>
#                         <td class="total">مجمـوع</td>
#                         <td></td>
#                     </tr>
#                 </thead>
#                 <tbody>

#                     {% for detail in order.orderdetail_set.all %}
#                     <tr>
#                         <td class="cart_product">
#                             <a href=""><img src="{{ detail.product.images.url }}" width="100" alt=""></a>
#                         </td>
#                         <td class="cart_description">
#                             <h4><a href="" class="one_line_text"> {{ detail.product.title }} </a></h4>
#                             <p>شناسـه : 01010101</p>
#                         </td>
#                         <td class="cart_price">
#                             <p> {{ detail.product.price|three_digits_currency }} </p>
#                         </td>
#                         <td class="cart_quantity">
#                             <div class="cart_quantity_button">
#                                 <a class="cart_quantity_up" href=""> + </a>
#                                 <input class="cart_quantity_input" type="text" name="quantity" value="1" autocomplete="off" size="2">
#                                 <a class="cart_quantity_down" href=""> - </a>
#                             </div>
#                         </td>
#                         <td class="cart_total">
#                             <p class="cart_total_price">{{ detail.get_total_price|three_digits_currency }}</p>
#                         </td>
#                         <td class="cart_delete">
#                             <a class="cart_quantity_delete" onclick="removeOrderDetail( {{detail.id}} )"><i class="fa fa-times"></i></a>
#                         </td>
#                     </tr>
#                     {% endfor %}

  
#                 </tbody>
#             </table>
#         </div>
#     </div>
# </section> <!--/#cart_items-->




# <section id="do_action">
#     <div class="container">
#         <div class="heading">
#             <h3>نهایی کردن سفارش یا ادامه خریـد ؟! </h3>
#             <p>در صورتیکـه کوپن خریـد و یا کد تخفیف داریـد میتوانید از آن استفاده نمایید | با استفاده از بخش مربوطه هزینه حمل و نقل خود را محاسبـه نمایید</p>
#         </div>
#         <div class="row">
#             <!-- <div class="col-sm-6">
#                 <div class="chose_area"> -->
#                     <!-- <ul class="user_option">
#                         <li>
#                             <h3>استفاده از کوپـن خریـد / کارت تخفیـف :</h3>
#                         </li>
#                         <li class="single_field zip-field">
#                             <input type="text" placeholder="کد تخفیف خود را وارد نمایید ...">
#                         </li>
#                         <li>
#                             <a class="btn btn-default update" href="">بررسی و اعمال</a>
#                         </li>
#                     </ul> -->


#                     <!-- <ul class="user_info">
#                         <h3>محاسبـه هزینـه حمل و نقل</h3>
#                         <li class="single_field">
#                             <label>استان :</label>
#                             <select>
#                                 <option>تهـران</option>
#                                 <option>اصفهان</option>
#                                 <option>آذربایجان غربـی</option>
#                                 <option>آذربایجان شرقـی</option>
#                             </select>
                            
#                         </li>
#                         <li class="single_field">
#                             <label>شهر / منطقه</label>
#                             <select>
#                                 <option>تهران</option>
#                                 <option>اصفهان</option>
#                                 <option>خـوی</option>
#                                 <option>تبریـز</option>
#                             </select>
                        
#                         </li>
#                         <li class="single_field zip-field">
#                             <label>کد پستی :</label>
#                             <input type="text">
#                         </li>
#                     </ul> -->
#                     <!-- <a class="btn btn-default update" href="">محاسبـه هزینـه حمل و نقـل</a> -->
#                 <!-- </div> -->
#             </div>
#             <div class="col-sm-6">
#                 <div class="total_area">
#                     <ul>
#                         <li>مجمـوع سبـد خریـد <span>{{ sum| three_digits_currency }}</span></li>
#                         <!-- <li>مالیـات (9%) <span>182.700 ريال</span></li>
#                         <li>هزینـه حمل و نقـل <span>رایـگان</span></li>
#                         <li>مجمـوع <span>2.212.700 ريال</span></li> -->
#                     </ul>
#                         <a class="btn btn-default update" href="shop.html">به روز رسانی سبـد خریـد </a>
#                         <a class="btn btn-default check_out" href="checkout.html">پرداخت</a>
#                 </div>
#             </div>
#         </div>
#     </div>
# </section><!--/#do_action-->


# </div>













# User_Basket.html

