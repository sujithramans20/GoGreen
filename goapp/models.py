from distutils.command.upload import upload
from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from django.db import models

class login(models.Model):
    login_id=models.AutoField(primary_key=True)
    email=models.EmailField(max_length=40)
    password=models.CharField(max_length=100)
    status=models.BooleanField(default=True)
    utype = models.IntegerField(default=2)  

class user(models.Model):
    user_id=models.AutoField(primary_key=True)
    Name=models.CharField(max_length=30)
    email=models.EmailField(max_length=30)
    mobile=models.CharField(max_length=30)
    address=models.CharField(max_length=30)
    image=models.ImageField(upload_to=None, height_field=None, max_length=100, null=True)
    login=models.ForeignKey(login, on_delete=models.CASCADE) #setting foreign key
    status=models.BooleanField(default=True)
    promote=models.BooleanField(default=False,null=True)

# class District(models.Model):
#     name=models.CharField(max_length=30)
     
#     def __str__(self):
#         return self.name

# class City(models.Model):
#     district= models.ForeignKey(District, on_delete=models.CASCADE)
#     name=models.CharField(max_length=30)

#     def __str__(self):
#         return self.name
class district(models.Model):
    dis=models.IntegerField(primary_key=True)
    dname=models.CharField(max_length=100)
    class meta:
        db_table="district"
class product(models.Model):
    p_id=models.AutoField(primary_key=True)
    pname=models.CharField(max_length=30)
    dis=models.CharField(max_length=30)
    image=models.ImageField(upload_to=None, height_field=None, max_length=100)
    quantity=models.IntegerField(default=3)
    price=models.FloatField(max_length=30, null=True)

class evaluator(models.Model):
    e_id=models.AutoField(primary_key=True)
    evname=models.CharField(max_length=30)
    email=models.EmailField(max_length=30)
    phone=models.CharField(max_length=10)
    address=models.CharField(max_length=100)
    district=models.ForeignKey(district,on_delete=models.CASCADE,null=True)
    city=models.CharField(max_length=30)
    password=models.CharField(max_length=30,null=True)
    login=models.ForeignKey(login,on_delete=models.CASCADE,null=True)
    
    
class adslot(models.Model):
    s_id=models.AutoField(primary_key=True)
    district=models.ForeignKey(district,on_delete=models.CASCADE,null=True)
    city=models.CharField(max_length=30)
    evname=models.CharField(max_length=30)
    date=models.DateField(max_length=30)
    time=models.TimeField(max_length=30)
    login=models.ForeignKey(login, on_delete=models.CASCADE) #setting foreign key
    res=models.CharField(max_length=30,null=True)
    advise=models.CharField(max_length=100,null=True)
    e=models.ForeignKey(evaluator,on_delete=models.CASCADE, null=True)
    

        
class city(models.Model):
    cit=models.IntegerField(primary_key=True)
    cname=models.CharField(max_length=100)
    dis=models.ForeignKey(district,on_delete=models.CASCADE,null=True)
    class meta:
        db_table="city"

class cart(models.Model):
    cartid=models.AutoField(primary_key=True)
    user=models.ForeignKey(user,on_delete=models.CASCADE,null=True)
    p=models.ForeignKey(product,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField( null=True)
    uprice=models.FloatField(null=True)
    tprice=models.FloatField(null=True)

class tbl_bank(models.Model):
    b_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(user,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=30,null=True)
    card=models.CharField(max_length=16)
    cvv=models.IntegerField()
    expry=models.CharField(max_length=30)

class order(models.Model):
    order_id=models.AutoField(primary_key=True)
    b=models.ForeignKey(tbl_bank,on_delete=models.CASCADE,null=True)
    transid=models.CharField(max_length=35,null=True)
    date=models.DateField(auto_now_add=True)
    amount=models.FloatField()
    user=models.ForeignKey(user,on_delete=models.CASCADE,null=True)
    status=models.CharField(default="ordered",max_length=30)
    track=models.CharField(max_length=40,null=True)
    
class orderdetails(models.Model):
    ord_id=models.AutoField(primary_key=True)
    order=models.ForeignKey(order,on_delete=models.CASCADE,null=True)
    p=models.ForeignKey(product,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()
    price=models.FloatField()
    status=models.CharField(max_length=30,default="ordered")
    

class culti(models.Model):
    ct_id=models.AutoField(primary_key=True)
    vname=models.CharField(max_length=30)
    dise=models.CharField(max_length=40)
    sdate=models.DateField()
    ldate=models.DateField()
    slot=models.ForeignKey(adslot,on_delete=models.CASCADE, null=True)
    status=models.CharField(max_length=40)
    login=models.ForeignKey(login, on_delete=models.CASCADE)
    e=models.ForeignKey(evaluator,on_delete=models.CASCADE, null=True)
    
    
    
    

    
    

