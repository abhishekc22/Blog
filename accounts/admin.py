from django.contrib import admin
from accounts.models import Blog, User, Comments, Response

# Register your models here.

admin.site.register(Blog)
admin.site.register(Comments)
admin.site.register(Response)
