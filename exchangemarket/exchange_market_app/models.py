# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Comments(models.Model):
    comment = models.TextField(blank=True, null=True)
    offer = models.ForeignKey('Offers', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comments'


class Inventories(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'inventories'


class Items(models.Model):
    id = models.IntegerField(primary_key=True)
    inventory = models.ForeignKey(Inventories, models.DO_NOTHING)
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'items'
        unique_together = (('id', 'inventory'),)


class OfferItems(models.Model):
    item = models.ForeignKey(Items, models.DO_NOTHING)
    item_inventory = models.ForeignKey(Items, models.DO_NOTHING)
    offer = models.ForeignKey('Offers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'offer_items'


class OfferUsers(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    offer = models.ForeignKey('Offers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'offer_users'


class Offers(models.Model):

    class Meta:
        managed = False
        db_table = 'offers'


class Users(models.Model):
    name = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    username = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
