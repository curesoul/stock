from django.contrib.auth.models import User
from django.db.models import Sum

from django.db import models


class Vendor(models.Model):
    vendor_name = models.CharField(max_length=128, verbose_name='供货商')

    class Meta:
        verbose_name = verbose_name_plural = '供货商'

    def __str__(self):
        return self.vendor_name


class Buyer(models.Model):
    buyer_name = models.CharField(max_length=128, verbose_name='采购人')
    department = models.CharField(max_length=128, verbose_name='部门/职位')

    class Meta:
        verbose_name = verbose_name_plural = '采购人'

    def __str__(self):
        return self.buyer_name


class Consignee(models.Model):
    consignee_name = models.CharField(max_length=128, verbose_name='使用人')
    consignee_company = models.CharField(max_length=128, verbose_name='公司名称')

    class Meta:
        verbose_name = verbose_name_plural = '使用人'

    def __str__(self):
        return self.consignee_name


class Position(models.Model):
    position_title = models.CharField(max_length=128, verbose_name='使用地点')
    comment = models.CharField(max_length=612, verbose_name='地点备注', blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_plural = '使用地点'

    def __str__(self):
        return self.position_title


class Purpose(models.Model):
    purpose_title = models.CharField(max_length=128, verbose_name='使用目的')
    comment = models.CharField(max_length=612, verbose_name='目的备注', blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_plural = '使用目的'

    def __str__(self):
        return self.purpose_title


class ItemSum(models.Manager):
    def get_queryset(self):
        return super(ItemSum, self).outs.aggregate(Sum('quantities')).get('quantities__sum')


class Item(models.Model):
    item_name = models.CharField(max_length=128, verbose_name='品名')
    pattern = models.CharField(max_length=64, verbose_name='型号')
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='单价')
    stocks = models.IntegerField(default=0, verbose_name='库存数量')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name='供货商')
    is_screen = models.BooleanField(default=False, verbose_name='是否显示屏')
    show_item = models.BooleanField(default=False, verbose_name='展示该项')
    # item_sum = ItemSum

    # def item_ins(self, obj):
    #     return obj.ins.aggregate(Sum('quantities')).get('quantities__sum')
    # item_ins.short_description = '入库总数'

    class Meta:
        verbose_name = verbose_name_plural = '1.配件表'

    def __str__(self):
        return self.item_name


class In(models.Model):
    in_date = models.DateTimeField(verbose_name='入库时间')
    recorder = models.ForeignKey(User, verbose_name='记录人', on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.CharField(max_length=612, verbose_name='入库备注', blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='货号', related_name='ins')
    buyer = models.ForeignKey(Buyer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='采购人')
    quantities = models.IntegerField(verbose_name='数量')
    purpose = models.ForeignKey(Purpose, verbose_name='目的', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_plural = '2.入库'


class Out(models.Model):
    out_date = models.DateTimeField(verbose_name='出库时间')
    recorder = models.ForeignKey(User, verbose_name='记录人', on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.CharField(max_length=612, verbose_name='出库备注', blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='型号', related_name='outs')
    consignee = models.ForeignKey(Consignee, on_delete=models.CASCADE, verbose_name='使用人')
    quantities = models.IntegerField(verbose_name='出库数量')
    purpose = models.ForeignKey(Purpose, verbose_name='使用目的', on_delete=models.CASCADE)
    position = models.ForeignKey(Position, verbose_name='使用地点', on_delete=models.CASCADE)

    class Meta:
        verbose_name = verbose_name_plural = '3.出库'


# class Stocks(models.Model):
#     item = models.ForeignKey(Item, verbose_name='品名', on_delete=models.CASCADE)
#     stocks = models.IntegerField(verbose_name='库存数量')
#
#     def __str__(self):
#         return self.item

