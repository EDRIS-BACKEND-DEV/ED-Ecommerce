from django.urls import path
from .views import ContactUsView, CreateProfileView, ListProfileView

urlpatterns = [
    # path('', contact_page, name='contact_us_page'),
    path('', ContactUsView.as_view(), name='contact_us_page'),
    path('create-profile/', CreateProfileView.as_view(), name='create_profile_page'),
    path('profile', ListProfileView.as_view(), name='user_profile')
]

