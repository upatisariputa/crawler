from django.db import models

# Create your models here.


class Videos(models.Model):
    title = models.CharField(max_length=50)
    update_date = models.DateField(null=True, blank=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    platfrom = models.CharField(max_length=10)

    # def __str__(self):
    #     return self.title


class Users(models.Model):
    image = models.CharField(max_length=500)
    user_name = models.CharField(max_length=50)
    signup_date = models.DateField(null=True, blank=True)
    user_info = models.TextField()
    subscribers_count = models.IntegerField(default=0)
