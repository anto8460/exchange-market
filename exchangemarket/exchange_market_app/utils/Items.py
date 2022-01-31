from enum import Enum
from exchange_market_app import models

class ItemsState(Enum):
    ITEM_CREATED = 0

class Items:

    @staticmethod
    def get_all_items():
        return list(models.Items.objects.all())

    @staticmethod
    def create_item(user_id, name, description):
        user = models.Users.objects.filter(id=user_id)
        inventory = models.Inventories.objects.filter(user=user[0].id)
        print(inventory)
        item = models.Items.objects.create(
            inventory=inventory[0],
            name=name,
            description=description
        )
        return ItemsState.ITEM_CREATED