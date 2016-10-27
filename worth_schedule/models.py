from django.db import models

# Create your models here.

class Currency(models.Model):
	name = models.CharField(max_length=50)
	ratioToDollars = models.FloatField()

class Event(models.Model):
	name = models.CharField(max_length=200)
	dueDate = models.DateTimeField()
	timeCost = models.FloatField()
	worth = models.BigIntegerField()
	currency = models.ForeignKey(Currency)
	#cost = models.BigIntegerField()
	#costCurrency = models.ForeignKey(Currency)

#def inDollars(amount, currency)
#	return currency.ratioToDollars * amount
