
from enum import Enum
from django.http import HttpResponseRedirect
from exchange_market_app.models import Users, Offers, Inventories, Items

class UserStates(Enum):
    AUTHENTICATED = 1
    WRONG_CREDENTIALS = 2
    EXCEED_TRIES =  3

class User:

    counter = 0

    def __init__(self):
        self._email = None
        self._pass = None
        self._is_authenticated = False
        self._data = None

    @staticmethod
    def reload_counter():
        User.counter = 0

    def authenticate(self, email, password):
        user = list(Users.objects.filter(email=email))

        if User.counter < 2 :
            # User does not exist
            if len(user) == 0:
                User.counter += 1
                self._is_authenticated = False
                return UserStates.WRONG_CREDENTIALS
            else:
                User.counter +=1
                if user[0].password == password:
                    self._is_authenticated = True
                    self._email = email
                    self._pass = password
                    self._data = user
                    return UserStates.AUTHENTICATED
                else:
                    self._is_authenticated = False
                    return UserStates.WRONG_CREDENTIALS
    
        return UserStates.EXCEED_TRIES
                
    def is_authenticated(self):
        return self._is_authenticated

    def get_primary_key(self):
        if self._data is None:
            return None
        return self._data[0].id