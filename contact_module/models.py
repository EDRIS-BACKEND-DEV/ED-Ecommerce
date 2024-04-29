from django.db import models

# Create your models here.


class ContactUs(models.Model):
    title = models.CharField(max_length=130)
    Email = models.EmailField(max_length=130)
    Name_and_Surname = models.CharField(max_length=130)
    Message = models.TextField(max_length=300)
    Date = models.DateTimeField(auto_now_add=True)
    admin_response = models.TextField(blank=True, null=True)
    is_read_by_admin = models.BooleanField(null=True, blank=True, default=False)

    class Meta:
        verbose_name = 'Contact Page'
        verbose_name_plural = 'Contact Page'

    def __str__(self):
        return self.title
    


# class UserProfileModels(models.Model):
#     images = models.FileField(upload_to='images')
    

class UserProfile(models.Model):
    image = models.ImageField(upload_to='images')


 
