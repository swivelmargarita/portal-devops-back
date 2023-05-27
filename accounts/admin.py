from django.contrib import admin
from .models import User, VerifyPhone


@admin.register(VerifyPhone)
class Admin(admin.ModelAdmin):
    list_display = ['phone', 'code']


admin.site.register(User)
