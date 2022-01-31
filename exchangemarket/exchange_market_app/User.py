
from enum import Enum
from django.http import HttpResponseRedirect
from exchange_market_app.models import Users, Offers, Inventories, Items


class UserStates(Enum):
    AUTHENTICATED = 1
    WRONG_CREDENTIALS = 2
    EXCEED_TRIES =  3

class User:

    data = None

    @staticmethod
    def set_counter(counter):
        User.counter = counter

    @staticmethod
    def authenticate(email, password):
        user = list(Users.objects.filter(email=email))
            # User does not exist
        if len(user) == 0:
            return UserStates.WRONG_CREDENTIALS
        else:
            if user[0].password == password:
                User.data = user
                return UserStates.AUTHENTICATED
            else:
                return UserStates.WRONG_CREDENTIALS

    @staticmethod
    def get_primary_key():
        if User.data is None:
            return None
        return User.data[0].id

    @staticmethod
    def get_inventory_items(user_id):
        user = Users.objects.filter(id=user_id)
        inventory = Inventories.objects.filter(user=user_id)
        items = Items.objects.filter(inventory=inventory[0].id)
        return items