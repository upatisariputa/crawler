from django.contrib import admin
from .models import Videos
from .models import Users
from .models import Post

# Register your models here.

admin.site.register(Videos)
admin.site.register(Users)
admin.site.register(Post)
