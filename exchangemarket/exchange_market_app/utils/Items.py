from exchange_market_app import models


class Items:

    @staticmethod
    def get_all_items():
        return list(models.Items.objects.all())