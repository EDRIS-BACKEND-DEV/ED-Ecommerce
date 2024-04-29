from django.urls import path
from .views import add_to_product, request_payment, verify_payment

urlpatterns = [
    path('add-to-order', add_to_product, name='add-to-order'),
    path('request-payment/', request_payment, name='request'),
    path('verify-payment/', verify_payment, name='verify'),
]


