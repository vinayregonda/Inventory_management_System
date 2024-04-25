from django.db import models
from datetime import datetime

# Create your models here.

class ims_customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    mobile = models.BigIntegerField()
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class ims_category(models.Model):
    categoryid = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=200,default=True)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=8, choices=STATUS_CHOICES,default=True)

    def __str__(self):
        return self.c_name

class ims_brand(models.Model):
    categoryid=models.ForeignKey(ims_category,on_delete=models.CASCADE)
    bname=models.CharField(max_length=250)
    status=models.BooleanField(default=True)
    
    def __str__(self):
        return self.bname
    
class ims_supplier(models.Model):
    supplierid=models.AutoField(primary_key=True)
    suppliername=models.CharField(max_length=200)
    mobile=models.BigIntegerField()
    address=models.TextField()
    status=models.BooleanField(default=True)

    def __str__(self):
        return self.suppliername

class ims_product(models.Model):
    pid=models.AutoField(primary_key=True)
    categoryid=models.ForeignKey(ims_category,on_delete=models.CASCADE)
    brandid=models.ForeignKey(ims_brand,on_delete=models.CASCADE)
    pname=models.CharField(max_length=300)
    model=models.CharField(max_length=250)
    description=models.TextField()
    quantity=models.BigIntegerField()
    unit=models.CharField(max_length=150)
    base_price= models.DecimalField(max_digits=10, decimal_places=2)
    tax= models.DecimalField(max_digits=4, decimal_places=2)
    supplier=models.ForeignKey(ims_supplier,on_delete=models.CASCADE)
    status=models.BooleanField(default=True)
    date=models.DateTimeField() 

    def __str__(self):
        return self.pname
    
class ims_purchase(models.Model):
    purchase_id=models.AutoField(primary_key=True)
    supplier_id=models.ForeignKey(ims_supplier,on_delete=models.CASCADE)
    product_id=models.ForeignKey(ims_product,on_delete=models.CASCADE)
    quantity=models.CharField(max_length=255)
    purchase_date=models.DateTimeField(auto_now_add=True)

class ims_order(models.Model):
    order_id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(ims_product,on_delete=models.CASCADE)
    total_shiped=models.IntegerField()
    cutomer_id=models.ForeignKey(ims_customer,on_delete=models.CASCADE)
    order_date=models.DateTimeField(auto_now_add=True)
    

