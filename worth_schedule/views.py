from django.shortcuts import render
from django.http import HttpResponse
from worth_schedule.models import *
from datetime import datetime, timedelta
from dateutil import parser

# Create your views here.

def inDollars(amount, currency):
	return amount * currency.ratioToDollars

def impossible(e):
	"This weeds out any events past their due date, with too little time to complete, etc."
	return True

def urgencyThenWorth(event1, event2):
	"""Sorts the two events based on these criteria:
		If event1 is due before event2, and if event2 is worth more than event1
		event1's time + event2's time is still before event2's deadline, then event1.
		Otherwise, event2"""
	if inDollars(event1.worth, event1.currency) > inDollars(event2.worth, event2.currency):
		if event1.dueDate < event2.dueDate:
			return 1
		elif (datetime.now() + timedelta(hours=event2.timeCost+event1.timeCost) < event1.dueDate and 
			datetime.now() + timedelta(hours=event1.timeCost) > event2.dueDate):
			return -1
	else:
		if event2.dueDate < event1.dueDate:
			return -1
		elif (datetime.now() + timedelta(hours=event2.timeCost+event1.timeCost) < event2.dueDate and
			datetime.now() + timedelta(hours=event2.timeCost) > event1.dueDate):
			return 1

def format(e):
	return (e.name + " - worth: " + str(e.worth) + " " +
		e.currency.name + "(" + 
		str(inDollars(e.worth, e.currency)) + " dollars)" +
		" - due: " + str(e.dueDate) + "<\br>")

def ranking_page(url):
	response = ""
	eventList = [x for x in Event.objects.all()]
	filter(impossible, eventList)
	eventList = sorted(eventList, cmp=urgencyThenWorth)
	for e in eventList:
		response += format(e)
	return HttpResponse(response)


def add_currency_raw(url, name, worthInDollars):
	p = Currency.objects.get_or_create(name=name, ratioToDollars=float(worthInDollars))[0]
	p.save()
	return HttpResponse("Currency added!")
	
def add_event_raw(url, name, due, time, worth, currency):
	c = Currency.objects.get(name=currency)
	p = Event.objects.get_or_create(name=name, dueDate=parser.parse(due), timeCost=float(time), worth=int(worth), currency=c)[0]
	p.save()
	return HttpResponse("Event added!")
