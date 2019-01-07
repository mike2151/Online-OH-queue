from django.contrib import admin
from .models import OHQueue


class OHQueueAdmin(admin.ModelAdmin):
    model = OHQueue
    fieldsets = (
        ('Basic Information:', {'fields': ('name',)}),
        ('Times Open:', {'fields': ('monday_times', 'tuesday_times', 'wednesday_times', 'thursday_times', 'friday_times', 'saturday_times', 'sunday_times'),
        'description': 'See github.com/mike2151/Online-OH-queue#OHQueueSetUp for how to format schedules.'}),
    )

admin.site.register(OHQueue, OHQueueAdmin)
