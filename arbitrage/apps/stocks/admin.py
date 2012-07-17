from django.contrib import admin
from .models import Stock, StockGroup


class StockAdmin(admin.ModelAdmin):
    readonly_fields = ('symbol', 'last_trade', 'bid', 'ask')
    list_display = ('symbol', 'site', 'last_trade')


class StockGroupAdmin(admin.ModelAdmin):
    pass
admin.site.register(Stock, StockAdmin)
admin.site.register(StockGroup, StockGroupAdmin)
