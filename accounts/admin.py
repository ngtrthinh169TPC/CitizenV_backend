from django.contrib import admin

from .models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'managed_by', 'user', 'permission',
                    'name_of_unit', 'classification', 'entry_permit', 'progress')


admin.site.register(Account, AccountAdmin)
