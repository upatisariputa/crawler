from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        """A string representation of the model."""
        return self.title


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
    image_url = models.URLField(max_length=400, blank=True)
    user_name = models.CharField(max_length=50)
    signup_date = models.DateField(null=True, blank=True)
    user_info = models.TextField()
    subscribers_count = models.IntegerField(default=0)
