from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return "<User: {} {}".format(self.email, self.password)

class Item(models.Model):
    
    label = models.CharField(max_length = 255)
    uploader = models.ForeignKey(User, related_name = "uploads")
    items = models.ManyToManyField(User, related_name= "users")
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
