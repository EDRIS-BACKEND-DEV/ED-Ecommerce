from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from product_module.models import Product
from .models import Order, OrderDetail
from django.urls import reverse
from django.conf import settings
import requests


# Create your views here.


def add_to_product(request:HttpRequest):
    product_id = int(request.GET.get('product_id'))
    count = int(request.GET.get('count'))
    
    if count < 1:
        return JsonResponse({
            'status':'invalid_count',
            'text':'مقدار وارد شده یافت نمیباشد',
            'icon':'warning',
            'confirm_button_text': "دیدم میگم",

        })



    print(f'product id is : {product_id} and count is : {count}')

    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id, is_active=True).first()
        if product is not None:
            # get current user open order cart
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)

    # now we have to check that does the current product exist in the order detail cart
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.count += count
                current_order_detail.save()
            else:
                new_detail = OrderDetail(order_id=current_order.id, product_id=product_id, count=count)
                new_detail.save()

            return JsonResponse({
                'status':'success',
                'text': "محصول با موفقیت به سبد خرید شما اضافه شد",
                'icon':'success',
                'confirm_button_text':'مرسیییی'
                
            })
                

            # add product to order cart
            ...

        else:
            return JsonResponse({
                'status':'not_found',
                'text':'محصول مورد نظر یافت نشد',
                'confirm_button_text':'مرسیییی',
                'icon':'error'
            })   
    else:
        return JsonResponse({
            'status':'user_not_auth',
            'text':'برای افزودن محصول به سبد خرید باید وارد سایت شوید, میبخشین دیگه',
            'confirm_button_text':'ورود به سایت',
            'icon':'error'
        })
    


def add_product_to_order(request: HttpRequest):
    product_id = int(request.GET.get('product_id'))
    count = int(request.GET.get('count'))
    if count < 1:
        # count = 1
        return JsonResponse({
            'status': 'invalid_count',
            'text': 'مقدار وارد شده معتبر نمی باشد',
            'confirm_button_text': 'مرسی از شما',
            'icon': 'warning'
        })

    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()
        if product is not None:
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.count += count
                current_order_detail.save()
            else:
                new_detail = OrderDetail(order_id=current_order.id, product_id=product_id, count=count)
                new_detail.save()

            return JsonResponse({
                'status': 'success',
                'text': 'محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد',
                'confirm_button_text': 'باشه ممنونم',
                'icon': 'success'
            })
        else:
            return JsonResponse({
                'status': 'not_found',
                'text': 'محصول مورد نظر یافت نشد',
                'confirm_button_text': 'مرسییییی',
                'icon': 'error'
            })
    else:
        return JsonResponse({
            'status': 'not_auth',
            'text': 'برای افزودن محصول به سبد خرید ابتدا می بایست وارد سایت شوید',
            'confirm_button_text': 'ورود به سایت',
            'icon': 'error'
        })










from django.conf import settings
import requests
import json


#? sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

# MERCHANT = 'test'
amount = 1000  # Rial / Re  quired
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/order/verify-payment/' 


def request_payment(request):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    if total_price == 0:
        return redirect(reverse('user_basket_page'))
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Description": description,
        # "Phone": phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    try:
        response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)

        print(response.text, 'this is our print')


        if response.status_code == 200:
            response_json = response.json()
            if response_json['Status'] == 100:
                return {'status': True, 'url': ZP_API_STARTPAY + str(response_json['Authority']), 'authority': response_json['Authority']}
            else:
                return {'status': False, 'code': str(response_json['Status'])}
        # return response
        return {'status': False, 'code': 'unexpected response', 'response': response.text}



    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}





from django.http import JsonResponse

def verify_payment(request):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()

    # Retrieve the authority from the request (you may need to adjust this based on your implementation)
    authority = request.GET.get('authority')

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total_price * 10,
        "Authority": authority,
    }
    headers = {'content-type': 'application/json', 'content-length': str(len(data)) }

    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if response_data['Status'] == 100:
            return JsonResponse({'status': True, 'RefID': response_data['RefID']})
        else:
            return JsonResponse({'status': False, 'code': str(response_data['Status'])})
    else:
        return JsonResponse({'status': False, 'error': 'Failed to verify payment'})









# from django.http import HttpRequest, JsonResponse, HttpResponse
# from product_module.models import Product
# from .models import Order, OrderDetail
# from django.shortcuts import redirect
# import requests
# import json














# # MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXXXXXX'
# MERCHANT = 'Ed Merchant'

# ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
# ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
# ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
# amount = 11000  # Rial / Required
# description = "نهایی کردن خرید شما از سایت ما"  # Required
# email = ''  # Optional
# mobile = ''  # Optional
# # Important: need to edit for realy server.
# CallbackURL = 'http://localhost:8000/order/verify-payment/'



# def request_payment(request: HttpRequest):
    
#     current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
#     total_price = current_order.calculate_total_price()
#     if total_price == 0:
#         return redirect(reverse('user_basket_page'))

#     req_data = {
#         "merchant_id": MERCHANT,
#         "amount": amount,
#         "callback_url": CallbackURL,
#         "description": description,
#         # "metadata": {"mobile": mobile, "email": email}
#     }
#     req_header = {"accept": "application/json", "content-type": "application/json'"}
#     req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
#     authority = req.json()['data']['authority']
#     if len(req.json()['errors']) == 0:
#         return redirect(ZP_API_STARTPAY.format(authority=authority))
#     else:
#         e_code = req.json()['errors']['code']
#         e_message = req.json()['errors']['message']
#         return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


# def verify_payment(request: HttpRequest):
#     print(request.user.id)
#     print(request.user)
    
#     current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
#     total_price = current_order.calculate_total_price()



#     t_authority = request.GET['Authority']
#     if request.GET.get('Status') == 'OK':
#         req_header = {"accept": "application/json", "content-type": "application/json'"}
#         req_data = {
#             "merchant_id": MERCHANT,
#             "amount": total_price * 10,
#             "authority": t_authority
#         }

#         req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
#         if len(req.json()['errors']) == 0:
#             t_status = req.json()['data']['code']
#             if t_status == 100:
#                 return HttpResponse('Transaction success.\nRefID: ' + str(
#                     req.json()['data']['ref_id']
#                 ))
#             elif t_status == 101:
#                 return HttpResponse('Transaction submitted : ' + str(
#                     req.json()['data']['message']
#                 ))
#             else:
#                 return HttpResponse('Transaction failed.\nStatus: ' + str(
#                     req.json()['data']['message']
#                 ))
#         else:
#             e_code = req.json()['errors']['code']
#             e_message = req.json()['errors']['message']
#             return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
#     else:
#         return HttpResponse('Transaction failed or canceled by user')


























