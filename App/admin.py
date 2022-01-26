from django.contrib import admin

# Register your models here.
from .models import Rules

class RulesAdmin(admin.ModelAdmin):
    list_display = ('high_risk_start', 'high_risk_end', 'medium_risk_start', 'medium_risk_end','low_risk_start', 'low_risk_end')

# Register your models here.

admin.site.register(Rules, RulesAdmin)