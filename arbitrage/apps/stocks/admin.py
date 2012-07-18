from django.contrib import admin
from .models import Stock, Group, StockGroup


class StockAdmin(admin.ModelAdmin):
    readonly_fields = ('symbol', 'last_trade', 'bid', 'ask')
    list_display = ('symbol', 'site', 'last_trade')


class StockGroupInline(admin.TabularInline):
    model = StockGroup
    extra = 1


class GroupAdmin(admin.ModelAdmin):
    inlines = (StockGroupInline,)
admin.site.register(Stock, StockAdmin)
admin.site.register(Group, GroupAdmin)
