from django.contrib import admin
from .models import UserProfile,AccessToken
from import_export.admin import ImportExportModelAdmin
# Register your models here.

admin.site.register(AccessToken)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name","username","user_type")

admin.site.register(UserProfile,UserProfileAdmin)