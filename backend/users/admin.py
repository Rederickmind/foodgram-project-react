from django.contrib import admin
from users.models import Subscription, User


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


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'author']
    search_fields = [
        'author__username',
        'author__email',
        'user__username',
        'user__email'
    ]
    list_filter = ['author__username', 'user__username']
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
