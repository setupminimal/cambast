from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from worth_schedule.models import *
from dateutil import parser
from worth_schedule.magic import sortTasks, inDollars

# Create your views here.

def impossible(e):
	"This weeds out any events past their due date, with too little time to complete, etc."
	return True

def ranking_page(request):
	eventList = [x for x in Event.objects.all()]
	filter(impossible, eventList)
	eventList = sortTasks(eventList)
	eventList = [(e, inDollars(e.worth, e.currency)) for e in eventList]
	template = loader.get_template('worth_schedule/index.html')
	cur = [x.name for x in Currency.objects.all()]
	context = RequestContext(request, { 'tasks': eventList,
						'currencies': cur })
	return HttpResponse(template.render(context))

def add_currency_raw(request):
	name = request.POST['name']
	worth = request.POST['worth']
	try:
		currency = request.POST['currency']
		c = Currency.objects.get(name=currency)
	except:
		c = Currency.objects.get_or_create(name="dollars", ratioToDollars=1)[0]
		c.save()
	p = Currency.objects.get_or_create(name=name, ratioToDollars=inDollars(float(worth), c))[0]
	p.save()
	return HttpResponseRedirect("/")
	
def add_event_raw(request):
	name = request.POST['name']
	due = request.POST['due']
	time = request.POST['time']
	worth = request.POST['worth']
	currency = request.POST['currency']
	c = Currency.objects.get(name=currency)
	p = Event.objects.get_or_create(name=name, dueDate=parser.parse(due), timeCost=float(time), worth=int(worth), currency=c)[0]
	p.save()
	return HttpResponseRedirect("/")

def finish(url, id):
	p = Event.objects.get(id=id).delete()
	return HttpResponseRedirect("/")
