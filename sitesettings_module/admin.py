from django.contrib import admin
from .models import SiteSettings, Slider, SiteBanner
# Register your models here.

class SliderAdmin(admin.ModelAdmin):
    list_display = ['slider_name', 'url', 'is_active']
    list_editable = ['is_active']

class SiteBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'position']

admin.site.register(SiteSettings)
admin.site.register(Slider, SliderAdmin)
admin.site.register(SiteBanner, SiteBannerAdmin)


