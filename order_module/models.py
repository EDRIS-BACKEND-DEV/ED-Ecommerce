from django.db import models
from account_module.models import User
from product_module.models import Product

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField()
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.user)
    
    def calculate_total_price(self):
        total_ammount = 0


        if self.is_paid:
            for order_detail in self.orderdetail_set.all():
                total_ammount += order_detail.final_price * order_detail.count
        else:
            for order_detail in self.orderdetail_set.all():
                total_ammount += order_detail.product.price + order_detail.count

        return total_ammount    
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    final_price = models.IntegerField(null=True, blank=True)
    count = models.IntegerField()

    def __str__(self):
        return str(self.order)
    
    def get_total_price(self):
        return self.count * self.product.price
    

    def calculate_total_price(self):
        total_ammount = 0


        if self.is_paid:
            for order_detail in self.orderdetail_set.all():
                total_ammount += order_detail.final_price * order_detail.count
        else:
            for order_detail in self.orderdetail_set.all():
                total_ammount += order_detail.product.price + order_detail.count

        return total_ammount

    
    class Meta:
        verbose_name = 'Order Detail'
        verbose_name_plural = 'Order Details'

