from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name')
    list_filter = ('email', 'username')
    search_fields = ('email', 'username')
    empty_value_display = '-пусто-'


admin.site.register(CustomUser, CustomUserAdmin)
