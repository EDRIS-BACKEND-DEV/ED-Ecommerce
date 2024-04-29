from django.db import models

# Create your models here.


class SiteSettings(models.Model):
    company_logo = models.ImageField(upload_to='images/company-logo', null=True)
    site_name = models.CharField(max_length=130, blank=True)
    site_url = models.CharField(max_length=130, blank=True)
    adress = models.CharField(max_length=130, blank=True)
    phone_sweden = models.CharField(max_length=130, blank=True)
    phone_iran = models.CharField(max_length=130, blank=True)
    fax = models.CharField(max_length=130, blank=True)
    email = models.CharField(max_length=130, blank=True)
    copy_right = models.TextField(max_length=130, blank=True)
    about_us_text = models.TextField(max_length=130, blank=True)
    site_logo = models.ImageField(max_length=130, blank=True)
    is_main_setting = models.BooleanField(blank=True)

    
    def __str__(self):
        return self.site_name
    


class Slider(models.Model):
    slider_name = models.CharField(max_length=130)
    url = models.URLField(max_length=130)
    url_title = models.CharField(max_length=130)
    description = models.TextField(max_length=130)
    image = models.ImageField(upload_to='images/sliders')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.slider_name


    class Meta:
        verbose_name = 'Slider'
 
    


class SiteBanner(models.Model):

    class SiteBannerPositions(models.TextChoices):
        product_list = 'product_list'
        product_detail = 'product_detail'
        about_us = 'about_us'

    title = models.CharField(max_length=200)
    url = models.URLField(max_length=400, null=True, blank=True)
    image = models.ImageField(upload_to='images/banners')
    is_active = models.BooleanField()
    position = models.CharField(max_length=200, choices=SiteBannerPositions.choices)



