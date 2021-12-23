from django.contrib import admin

from .models import Citizen


class CitizenAdmin(admin.ModelAdmin):
    list_display = ('citizen_id', 'managed_by', 'first_name',
                    'last_name', 'date_of_birth', 'place_of_birth')


admin.site.register(Citizen, CitizenAdmin)
