from django.db import models

# Create your models here.

<<<<<<< HEAD
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
=======
>>>>>>> 2dcecb88a785c836074a1a21c55ef7f3938716ff

class Platform(models.Model):
    P_key = models.AutoField(primary_key=True)
    P_url = models.CharField(max_length=100)
    P_userkey = models.IntegerField(default=0)
    P_name = models.CharField(max_length=10)
    objects = models.Manager()


class User_info(models.Model):
    U_key = models.AutoField(primary_key=True)
    U_name = models.CharField(max_length=20)
    U_img = models.CharField(max_length=100)
    U_info = models.CharField(max_length=100)
    U_sudate = models.CharField(max_length=20)
    P_key = models.ForeignKey(Platform, on_delete=models.CASCADE)
    objects = models.Manager()


class Subscribe(models.Model):
    S_key = models.AutoField(primary_key=True)
    created_at = models.CharField(max_length=15)
    S_count = models.IntegerField(default=0)
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=2)
    week = models.CharField(max_length=4)
    day = models.CharField(max_length=2)
    P_key = models.ForeignKey(Platform, on_delete=models.CASCADE)
    objects = models.Manager()


class Video(models.Model):
    V_key = models.AutoField(primary_key=True)
    V_name = models.CharField(max_length=100)
    V_upload = models.DateField(null=False)
    like_A_Y = models.IntegerField(default=0)
    dislike_Y = models.IntegerField(default=0)
    view_A_Y_T = models.IntegerField(default=0)
    comment_A_Y = models.IntegerField(default=0)
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=2)
    week = models.CharField(max_length=4)
    day = models.CharField(max_length=2)
    P_key = models.ForeignKey(Platform, on_delete=models.CASCADE)
    objects = models.Manager()


class Total(models.Model):
    T_key = models.AutoField(primary_key=True)
    T_like_count = models.IntegerField(default=0)
    T_unlike_count = models.IntegerField(default=0)
    T_view_count = models.IntegerField(default=0)
    T_update = models.DateField(null=False)
    P_key = models.ForeignKey(Platform, on_delete=models.CASCADE)
    objects = models.Manager()


class D_sub_gap(models.Model):
    SD_key = models.AutoField(primary_key=True)
    sub_count = models.IntegerField(default=0)
    P_key = models.ForeignKey(Platform, models.CASCADE)
    objects = models.Manager()


class W_sub_gap(models.Model):
    SW_key = models.AutoField(primary_key=True)
    sub_count = models.IntegerField(default=0)
    P_key = models.ForeignKey(Platform, models.CASCADE)
    objects = models.Manager()


class M_sub_gap(models.Model):
    SM_key = models.AutoField(primary_key=True)
    sub_count = models.IntegerField(default=0)
    P_key = models.ForeignKey(Platform, models.CASCADE)
    objects = models.Manager()


class D_video_gap(models.Model):
    VD_key = models.AutoField(primary_key=True)
    like_A_Y = models.IntegerField(default=0)
    dislike_Y = models.IntegerField(default=0)
    view_A_Y_T = models.IntegerField(default=0)
    comment_A_Y = models.IntegerField(default=0)
    P_key = models.ForeignKey(Platform, models.CASCADE)
    objects = models.Manager()


class W_video_gap(models.Model):
    VW_key = models.AutoField(primary_key=True)
    like_A_Y = models.IntegerField(default=0)
    dislike_Y = models.IntegerField(default=0)
    view_A_Y_T = models.IntegerField(default=0)
    comment_A_Y = models.IntegerField(default=0)
    P_key = models.ForeignKey(Platform, models.CASCADE)
    objects = models.Manager()


class M_video_gap(models.Model):
    VM_key = models.AutoField(primary_key=True)
    like_A_Y = models.IntegerField(default=0)
    dislike_Y = models.IntegerField(default=0)
    view_A_Y_T = models.IntegerField(default=0)
    comment_A_Y = models.IntegerField(default=0)
    P_key = models.ForeignKey(Platform, models.CASCADE)
    objects = models.Manager()
