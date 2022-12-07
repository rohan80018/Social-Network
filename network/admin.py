from django.contrib import admin
from .models import User, Data, Follow, Likes
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ["creater"]
class FollowAdmin(admin.ModelAdmin):
    list_display= ["user"]
class LikesAdmin(admin.ModelAdmin):
    list_display= ["liked_content"]

admin.site.register(User)
admin.site.register(Data, PostAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Likes, LikesAdmin)
