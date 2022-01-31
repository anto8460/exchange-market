from unittest import result
from django.test import TestCase
from exchange_market_app import models
from exchange_market_app.User import User, UserStates


# Create your tests here.


class UserClassTest(TestCase):

    def setUp(self) -> None:
        users = models.Users.objects.create(
            name="TestUser2",
            email="testuser2@test",
            country="Denmark",
            username= "TestUser2",
            password="test")

        inventory = models.Inventories.objects.create(
            user=users
        )
        item1 = models.Items.objects.create(
            inventory = inventory,
            name = "TestItem1",
            description = "This is test for Item",
            image = ""
        )
        item2 = models.Items.objects.create(
            inventory = inventory,
            name = "TestItem2",
            description = "This is test for Item",
            image = ""
        )

    def test_User_authenticate_correct_credentials(self):
        result = User.authenticate("testuser2@test", "test")
        expected = UserStates.AUTHENTICATED
        self.assertEqual( result, expected )

    def test_User_authenticate_wrong_email(self):
        result = User.authenticate("wrong@email", "test")
        expected = UserStates.WRONG_CREDENTIALS
        self.assertEqual( result, expected )

    def test_User_authenticate_wrong_password(self):
        result = User.authenticate("testuser2@test", "wrongpass")
        expected = UserStates.WRONG_CREDENTIALS
        self.assertEqual( result, expected )

    def test_User_get_inventory_correct_id(self):
        user = models.Users.objects.filter(name="TestUser2")
        inventory = models.Inventories.objects.filter(user=user[0].id)
        expected = models.Items.objects.filter(inventory=inventory[0].id)
        result = User.get_inventory_items(user_id=user[0].id)
        self.assertListEqual( list(result), list(expected) )

    def test_User_add_user_correct_input(self):
        name = "TestUser3"
        country = "Denmark"
        username = "UsernameTEST3"
        email =  "testuser3@test"
        password = "testpass"

        result = User.add_user(name, country, username, email, password)
        expected = UserStates.USER_CREATED

        self.assertEqual( result, expected )
    
    def test_User_add_user_existing_email(self):
        name = "TestUser3"
        country = "Denmark"
        username = "UsernameTEST3"
        email =  "testuser3@test"
        password = "testpass"

        User.add_user(name, country, username, email, password)
        username = "UsernameTEST4"
        result = User.add_user(name, country, username, email, password)
        expected = UserStates.USER_EXISTS

        self.assertEqual( result, expected )

    def test_User_add_user_existing_username(self):
        name = "TestUser3"
        country = "Denmark"
        username = "UsernameTEST3"
        email =  "testuser3@test"
        password = "testpass"

        User.add_user(name, country, username, email, password)
        result = User.add_user(name, country, username, email, password)
        expected = UserStates.USERNAME_EXISTS

        self.assertEqual( result, expected )
