# This is where a Cambast's magic happens.

from datetime import timedelta, datetime

workRatio = 24.0/10.0 # Working 10 hour days at most
# This ratio should be adjusted to account for how much
# time each day you're able to spend on the tasks that
# you manage with Cambast.

def inDollars(amount, currency):
	return amount * currency.ratioToDollars

def sortTasks(tasks):
	tasks = sorted(tasks, key=lambda e: inDollars(e.worth, e.currency))
	for j in range(len(tasks)):
		for i in range(len(tasks) - 1):
			if tasks[i+1].dueDate < tasks[i].dueDate:
				# "If task 2 is due before task 1 . . .
				now = datetime.now()
				until1 = (tasks[i].dueDate.replace(tzinfo=None) - now).total_seconds()/3600
				until1 *= workRatio # Number of working hours until task i
				if tasks[i+1].timeCost + tasks[i].timeCost < until1:
					# . . . and we can get them both done
					tasks[i], tasks[i+1] = tasks[i+1], tasks[i] # swap them
	return tasks
