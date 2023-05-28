from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name'
    )
    search_fields = ('username', 'email',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
