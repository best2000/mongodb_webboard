from django.contrib import admin
from core.models import *
# Register your models here.

admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(Create)
admin.site.register(Tag)
admin.site.register(LikeTopic)
admin.site.register(LikeComment)
