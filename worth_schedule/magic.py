# This is where a Cambast's magic happens.

from datetime import timedelta, datetime

workRatio = 24.0/(20.0/7.0) # Doing 4 hours of homework at most
# This ratio should be adjusted to account for how much
# time each day you're able to spend on the tasks that
# you manage with Cambast.

def mustBeDoneFirst(tasks, i, j):
	# j due before i?
	# time between now and i.dueDate to do j? (including time to do i)
	now = datetime.now()
	# untili represents how much working time we have before i is due.
	# This should eventually be modified to account for days of the week.
	untili = (tasks[i].dueDate.replace(tzinfo=None) - now).total_seconds()/3600.0
	untili *= workRatio
	return tasks[j].dueDate < tasks[i].dueDate and sum(map(lambda t: t.timeCost, tasks[:j])) < untili

def inDollars(amount, currency):
	return amount * currency.ratioToDollars

def sortTasks(tasks):
	tasks = sorted(tasks, key=lambda e: inDollars(e.worth, e.currency), reverse=True)
	for j in range(len(tasks)):
		for i in range(len(tasks) - 1):
			if mustBeDoneFirst(tasks, i, i+1):
				tasks[i], tasks[i+1] = tasks[i+1], tasks[i] # swap them
	return tasks
