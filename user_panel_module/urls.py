from django.urls import path
from .views import UserPanelView, EditUserProfileView, ChangePasswordView, user_basket, remove_order_detail, change_order_detail_count, UsersProducts, my_shopping_detail

urlpatterns = [
    path('', UserPanelView.as_view(), name='user_panel'),
    path('edit-profile', EditUserProfileView.as_view(), name='edit_user_profile'),
    path('change-pass', ChangePasswordView.as_view(), name='change_password_page'),
    path('user_basket', user_basket, name='user_basket_page'),
    path('remove-basket-detail', remove_order_detail, name='remove_order_detail'),
    # path('change-basket-detail', change_order_detail_count, name='change_basket_product')
    path('change-order-detail', change_order_detail_count, name='change_order_detail_count_ajax'),
    path('my-products/', UsersProducts.as_view(), name='user_bought_product_page'),
    path('my-shopping-detail/<order_id>', my_shopping_detail, name='user_shopping_detail_page'),

]


