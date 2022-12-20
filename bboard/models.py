from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    balance = models.FloatField(null=True,blank=True)
    published = models.DateTimeField(auto_now_add=True, db_index=True)


class StockRn(models.Model):
    nameCompany = models.CharField(max_length=20)
    currentPrice = models.FloatField(null=True, blank=True)
    published = models.DateTimeField(auto_now_add=True, db_index=True)


class PeriodStock(models.Model):
    CompanyName = models.CharField(max_length=20)
    Start = models.CharField(max_length=8)
    End = models.CharField(max_length=8)
    ChangedPrice = models.FloatField()

class pred(models.Model):
    Date = models.CharField(max_length=20)
    Price = models.FloatField(null=True,blank=True)

