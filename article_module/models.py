from django.db import models
from account_module.models import User
from jalali_date import date2jalali

# Create your models here.



class ArticleCategory(models.Model):
    parent = models.ForeignKey('ArticleCategory', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=130)
    url_title = models.CharField(max_length=130, unique=True)
    is_active = models.BooleanField(default=True, blank=True)

    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'ArticleCategory'
        verbose_name_plural = 'ArticleCategories'



class Article(models.Model):
    title = models.CharField(max_length=130)
    slug = models.SlugField(max_length=130)
    image = models.ImageField(upload_to='images/articles')
    short_description = models.TextField()
    text = models.TextField()
    is_active = models.BooleanField(default=True, blank=True)
    selected_categories = models.ManyToManyField(ArticleCategory)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, editable=False)
    create_date = models.DateTimeField(auto_now_add=True, editable=False)


    # def get_jalali_create_date(self):
    #     return date2jalali(self.create_date)
    
    # def get_jalali_create_time(self):
    #     return self.create_date.strftime('%H:%M')

    
    def __str__(self):
        return self.title
    

class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    parent = models.ForeignKey('ArticleComment', null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    class Meta: 
        verbose_name = 'Article Comment'
        verbose_name_plural = 'Article Comments'

    def __str__(self):
        return str(self.user)
        
 
    