from django.contrib import admin
from .models import profile,Post,like,Category,follewerCounts,Message

# Register your models here.
admin.site.register(profile)
admin.site.register(Post)
admin.site.register(like)
admin.site.register(Category)
admin.site.register(follewerCounts)
admin.site.register(Message)

