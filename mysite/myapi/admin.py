from django.contrib import admin
from .models import Platform
from .models import User_info
from .models import Subscribe
from .models import Video
from .models import Total
from .models import D_sub_gap
from .models import W_sub_gap
from .models import M_sub_gap
from .models import D_video_gap
from .models import W_video_gap
from .models import M_video_gap

# Register your models here.

admin.site.register(Platform)
admin.site.register(User_info)
admin.site.register(Subscribe)
admin.site.register(Video)
admin.site.register(Total)
admin.site.register(D_sub_gap)
admin.site.register(W_sub_gap)
admin.site.register(M_sub_gap)
admin.site.register(D_video_gap)
admin.site.register(W_video_gap)
admin.site.register(M_video_gap)
