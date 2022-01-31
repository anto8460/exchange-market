from unittest import result
from django.test import TestCase
from exchange_market_app import models
from exchange_market_app.User import User, UserStates
from exchange_market_app.utils.Items import Items, ItemsState


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


class ItemClassTest(TestCase):

    def setUp(self) -> None:
        users = models.Users.objects.create(
            name="TestUser2",
            email="testuser2@test",
            country="Denmark",
            username= "TestUser2",
            password="test")
        
        users2 = models.Users.objects.create(
            name="TestUser1",
            email="testuser1@test",
            country="Denmark",
            username= "TestUser1",
            password="test")

        inventory = models.Inventories.objects.create(
            user=users
        )
        inventory2 = models.Inventories.objects.create(
            user=users2
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
        item3 = models.Items.objects.create(
            inventory = inventory,
            name = "TestItem3",
            description = "This is test for Item",
            image = ""
        )

    def test_Items_get_all_items(self):
        result = Items.get_all_items()
        expected = list(models.Items.objects.all())

        self.assertListEqual(result, expected)

    def test_Items_create_item(self):
        user = models.Users.objects.filter(name="TestUser2")
        name = "testItemName"
        description = "testDescription"

        result = Items.create_item(user[0].id, name, description)
        expected = ItemsState.ITEM_CREATED

        self.assertEqual(result, expected)
    
    def test_Items_get_item(self):
        expected_item = models.Items.objects.filter(name="TestItem1")
        item, status = Items.get_item(expected_item[0].id)

        expected = [expected_item[0], ItemsState.ITEM_FOUND]
        result = [item[0], status]
        self.assertListEqual(expected, result)

    def test_Items_is_item_from_inventory_true(self):
        user = models.Users.objects.filter(name="TestUser2")
        item = models.Items.objects.filter(name="TestItem1")

        result = Items.is_item_from_inventory(item[0].id, user[0].id)
        expected = True

        self.assertEqual(expected, result)

    def test_Items_is_item_from_inventory_false(self):
        user = models.Users.objects.filter(name="TestUser1")
        item = models.Items.objects.filter(name="TestItem1")

        result = Items.is_item_from_inventory(item[0].id, user[0].id)
        expected = False

        self.assertEqual(expected, result)

    def test_Items_delete_item(self):
        item = models.Items.objects.filter(name="TestItem1")

        result = Items.delete_item(item[0].id)
        expected = ItemsState.ITEM_DELETED

        self.assertEqual(expected, result)

    def test_Items_delete_item_not_in_db(self):
        item = models.Items.objects.filter(name="TestItem3")
        item_id = item[0].id
        Items.delete_item(item[0].id)
        result = Items.delete_item(item_id)
        expected = ItemsState.ITEM_NOT_FOUND

        self.assertEqual(expected, result)

    def test_Items_edit_item(self):
        item = models.Items.objects.filter(name="TestItem2")
        result = Items.edit_item(item[0].id, "Edited", "Edited")
        expected = ItemsState.ITEM_EDITED
        
        self.assertEqual(expected, result)