from django.contrib import admin

from .models import Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'created_at',
                    'reporter', 'completed', 'account')


admin.site.register(Report, ReportAdmin)
