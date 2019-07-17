from django.contrib.auth.models import User
from django.contrib import admin
from django.utils import timezone
from django.db.models import Sum

from .models import Vendor, Item, Position, Purpose, In, Out, Buyer, Consignee


class ItemInVendor(admin.TabularInline):
    fields = ['item_name', 'pattern', 'price']
    model = Item


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['vendor_name']
    inlines = [ItemInVendor, ]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'pattern', 'vendor', 'item_ins', 'item_outs', 'item_quantity']

    def item_ins(self, obj):
        return obj.ins.aggregate(Sum('quantities')).get('quantities__sum')
    item_ins.short_description = '入库总数'

    def item_outs(self, obj):
        return obj.outs.aggregate(Sum('quantities')).get('quantities__sum')
    item_outs.short_description = '出库总数'

    def item_quantity(self, obj):
        if not self.item_ins(obj):
            return '-'
        if self.item_outs(obj):
            return self.item_ins(obj) - self.item_outs(obj)
        return '-'
    item_quantity.short_description = '库存数量'


    # def stock_sum(self, obj):
    #     if int(obj.in_set.aggregate(Sum('quantities')).get('quantities__sum')) != '':
    #         return int(obj.in_set.aggregate(Sum('quantities')).get('quantities__sum')) \
    #                - int(obj.out_set.aggregate(Sum('quantities')).get('quantities__sum'))
    #     else:
    #         return 0
    # stock_sum.short_description = '在库数'

    # def save_model(self, request, obj, form, change):
    #     obj.stocks = self.stock_sum()
    #     return super(ItemAdmin, self).save_model(request, obj, form, change)
    # def out_sum(self, obj):
    #     # outs = obj.out_set.aggregate(Sum('quantities')).get('quantities__sum')
    #     return obj.out_set.aggregate(Sum('quantities')).get('quantities__sum')
    # out_sum.short_description = '总出库数'

    # def stock_sum(self):
    #     return self.in_sum()[0] + self.out_sum()[0]
    # stock_sum.short_description = '当前库存'


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['position_title', 'comment']


@admin.register(Purpose)
class PurposeAdmin(admin.ModelAdmin):
    list_display = ['purpose_title', 'comment']


@admin.register(In)
class InAdmin(admin.ModelAdmin):
    model = Item
    list_display = ['in_date', 'item', 'item_name', 'quantities', 'purpose', 'recorder', 'buyer', 'comment']
    fields = ['item', 'buyer', 'quantities', 'purpose', 'comment']
    list_filter = ['in_date', 'item', 'purpose']
    search_fields = ['item']

    def item_price(self, obj):
        return obj.item.price
    item_price.short_description = '单价'
    item_price.admin_order_field = 'item'

    def item_name(self, obj):
        return obj.item.item_name
    item_name.short_description = '品名'

    def save_model(self, request, obj, form, change):
        obj.recorder = request.user
        obj.in_date = timezone.now()
        # obj.item.stocks = int(request.POST['quantities']) + obj.item.stocks
        return super(InAdmin, self).save_model(request, obj, form, change)


@admin.register(Out)
class OutAdmin(admin.ModelAdmin):
    model = Item, In, Out
    list_display = ['out_date', 'item', 'item_name', 'item_price', 'quantities', 'recorder',
                    'consignee', 'position', 'purpose', 'comment']
    fields = ['item', 'consignee', 'position', 'purpose', 'quantities', 'comment']
    raw_id_fields = ('position',)
    list_filter = ['out_date', 'item', 'purpose', 'consignee']
    search_fields = ['position__position_title', ]

    def item_price(self, obj):
        return obj.item.price

    item_price.short_description = '单价'
    item_price.admin_order_field = 'item'

    def item_name(self, obj):
        return obj.item.item_name

    item_name.short_description = '品名'

    def save_model(self, request, obj, form, change):
        obj.recorder = request.user
        obj.out_date = timezone.now()
        return super(OutAdmin, self).save_model(request, obj, form, change)


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ['buyer_name', 'department']


@admin.register(Consignee)
class ConsigneeAdmin(admin.ModelAdmin):
    list_display = ['consignee_name', 'consignee_company']
