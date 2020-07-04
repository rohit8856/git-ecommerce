from django.db import models

# Create your models here it is a schema for table.
class product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length =50,default="")
    subcategory = models.CharField(max_length =50,default="")
    price= models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images",default="")

    def __str__(self):
        return self.product_name

# you have to register your model in admin .py
class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length =50,default="")
    number= models.CharField(max_length=10,default=0)
    desc = models.CharField(max_length=300)
    

    def __str__(self):
        return self.name

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length = 111)
    number =models.CharField(max_length=11,default="")
    address = models.CharField(max_length=160)
    address2 = models.CharField(max_length=160,default="")
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)


class Orderupdate(models.Model):
    update_id = models.AutoField(primary_key = True)
    order_id = models.IntegerField(default='')
    update_desc =models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."