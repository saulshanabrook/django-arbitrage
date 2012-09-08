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

admin.site.register(Stock, StockAdmin)
admin.site.register(Group, GroupAdmin)
