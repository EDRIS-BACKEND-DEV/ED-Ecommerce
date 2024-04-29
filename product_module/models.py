from django.db import models
from account_module.models import User

# Create your models here.


from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class ProductCategory(models.Model):
    title = models.CharField(max_length=130, db_index=True)
    url_title = models.CharField(max_length=130, db_index=True)
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(null=True)


    def __str__(self):
        return self.title
    
    class Meta:
     verbose_name = 'Products Category'
     verbose_name_plural = 'Product  Category'
    

class ProductBrand(models.Model):
    title = models.CharField(max_length=130)
    url_title = models.CharField(max_length=300, db_index=True, null=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brand'

    def __str__(self):  
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=300)
    images = models.ImageField(null=True, upload_to='images/product')   
    price = models.IntegerField()
    short_description = models.CharField(max_length=300, null=True, db_index=True)
    description = models.CharField(max_length=300, null=True, db_index=True)
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(db_index=True, unique=True)
    category = models.ManyToManyField(ProductCategory, related_name='categories_products')
    is_delete = models.BooleanField(blank=True,null=True)
    Brand = models.ForeignKey(ProductBrand, null=True, on_delete=models.CASCADE, blank=True, default=True)



    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])


    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Product'



class ProductTag(models.Model):
    tag_caption = models.CharField(max_length=120, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags')


    def __str__(self):  
        return self.tag_caption
    
    class Meta:
        verbose_name='Product  Tag'
        verbose_name_plural = 'Product  Tag'



class ProductVisit(models.Model):
    product = models.ForeignKey('Product', null=True, on_delete=models.CASCADE)
    ip = models.CharField(max_length=30)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE )

    def __str__(self):
        return f'{self.product.title} / {self.ip}'
    
    class Meta:
        verbose_name = 'ProductVisit'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/product-gallery')

    def __str__(self):
        return self.product.title
    
    class Meta:
        verbose_name = 'Product Gallery'
        verbose_name_plural = 'Product Galleries'