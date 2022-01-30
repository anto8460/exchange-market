from exchange_market_app import models

def get_all_items():
    return list(models.Items.objects.all())