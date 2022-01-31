from enum import Enum
from exchange_market_app import models

class ItemsState(Enum):
    ITEM_CREATED = 0
    ITEM_NOT_FOUND = 1
    ITEM_FOUND = 2
    ITEM_DELETED = 3
    ITEM_EDITED = 4

class Items:

    @staticmethod
    def get_all_items():
        return list(models.Items.objects.all())

    @staticmethod
    def create_item(user_id, name, description, free):
        user = models.Users.objects.filter(id=user_id)
        inventory = models.Inventories.objects.filter(user=user[0].id)
        item = models.Items.objects.create(
            inventory=inventory[0],
            name=name,
            description=description,
            is_free=free
        )
        return ItemsState.ITEM_CREATED

    @staticmethod
    def get_item(item_id) -> list : 
        item = models.Items.objects.filter(id=item_id)

        if len(item) == 0:
            return [None, ItemsState.ITEM_NOT_FOUND]
        else:
            return [item, ItemsState.ITEM_FOUND]
    
    @staticmethod
    def is_item_from_inventory(item_id, user_id) -> bool:
        user = models.Users.objects.filter(id=user_id)
        item = models.Items.objects.filter(id=item_id)
        inventory = models.Inventories.objects.filter(user=user[0].id)

        if item[0].inventory == inventory[0]:
            return True
        else:
            return False

    @staticmethod
    def delete_item(item_id):
        deleted, item = models.Items.objects.filter(id=item_id).delete()
        if deleted:
            return ItemsState.ITEM_DELETED
        else:
            return ItemsState.ITEM_NOT_FOUND

    @staticmethod
    def edit_item(item_id, name, description, free):
        item =  models.Items.objects.get(id=item_id)
        item.name = name
        item.description = description
        item.is_free = free
        item.save()
        return ItemsState.ITEM_EDITED