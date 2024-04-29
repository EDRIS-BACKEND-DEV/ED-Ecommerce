from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group

# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/profile', null=True, blank=True)
    email_active_code = models.CharField(max_length=130, blank=True)
    about_user = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)




   # this is function which if first name or lastname didnt exist,
   #  it should return the email instead.
 
    def __str__(self):
        if self.first_name is not '' and self.last_name is not '':
            return self.get_full_name()
        
        
        return self.email
        

    
    

