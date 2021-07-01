from os import name
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class save_sum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=5000)
class all_sum(models.Model):
    link = models.CharField(max_length=200)
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=5000)
class Comment(models.Model):
    post = models.ForeignKey(all_sum,related_name="comments",on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

class ContactForm(models.Model):
    name = models.CharField(max_length=20)
    body = models.TextField()       
    