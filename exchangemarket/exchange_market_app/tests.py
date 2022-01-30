from unittest import result
from django.test import TestCase
from exchange_market_app import models
from exchange_market_app.User import User, UserStates
# Create your tests here.


class UserClassTest(TestCase):

    def setUp(self) -> None:
        models.Users.objects.using("exchange")
        users = models.Users.objects.create(
            name="TestUser2",
            email="testuser2@test",
            country="Denmark",
            username= "TestUser2",
            password="test")
        users.save()

    def test_User_authenticate_correct_credentials(self):
        user = User()
        result = user.authenticate("testuser2@test", "test")
        expected = UserStates.AUTHENTICATED
        self.assertEqual( result, expected )
