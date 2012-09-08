from django.contrib import admin
from .models import Stock, Group, StockGroup


class StockAdmin(admin.ModelAdmin):
    readonly_fields = ('symbol', 'buying', 'selling')
    list_display = ('symbol', 'site', 'buying', 'selling')

    def save_model(self, request, obj, form, change):
        obj.sync()
        obj.save()


class StockGroupInline(admin.TabularInline):
    model = StockGroup
    extra = 1


class GroupAdmin(admin.ModelAdmin):
    inlines = (StockGroupInline,)
    list_display = ['name', 'completion_date', 'greatest_difference', 'apr']
    actions = ['sync_stocks']

    def sync_stocks(self, request, queryset):
        message_bits = []
        for group in queryset:
            [stock.sync() for stock in group.stocks.all()]
            message_bits.append("{} stocks updated in {}".format(group.stocks.count(),
                                                            group))
        self.message_user(request, '\n'.join(message_bits))

admin.site.register(Stock, StockAdmin)
admin.site.register(Group, GroupAdmin)
