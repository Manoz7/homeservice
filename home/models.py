from functools import cache
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL

from django.contrib.auth.models import User


class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    content = models.TextField()
    timeStamp = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return "Message From " + self.name


class Status(models.Model):
    status = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.status


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='customer/', null=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=50)
    service_desc = models.TextField()
    image = models.FileField(null=True)
    pub_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.service_name


class Service_Man(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='service_man/', null=True)
    address = models.CharField(max_length=100, null=True)
    service = models.ForeignKey(
        Service, on_delete=CASCADE, null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class BookService(models.Model):
    book_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=50, default='')
    email = models.EmailField(max_length=20, default='')
    book_desc = models.TextField()
    book_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class BookUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    book_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=500)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:30] + "...."
