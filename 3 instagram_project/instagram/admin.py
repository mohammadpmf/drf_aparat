from django.contrib import admin

from .models import *

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Comment)
