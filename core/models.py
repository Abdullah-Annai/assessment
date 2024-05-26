from django.db import models
import uuid
# Create your models here.

class Account(models.Model):
    email = models.EmailField(unique=True)
    accound_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    name = models.CharField(max_length=100)
    secret_token = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    website = models.URLField(blank=True,null=True)


class Destination(models.Model):
    account = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='destination')
    url = models.URLField()
    http_method = models.CharField(max_length=10, choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT')])
    headers = models.JSONField()