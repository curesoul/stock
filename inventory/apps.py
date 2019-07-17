from django.apps import AppConfig


class InventoryConfig(AppConfig):
    name = 'inventory'

    def __str__(self):
        return '库存管理'
