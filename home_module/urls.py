
from django.urls import path, include
from .views import HomeView, About_us

urlpatterns = [
    path('', HomeView.as_view(), name='Home'),
    path('about/', About_us.as_view(), name='about_page')
]
