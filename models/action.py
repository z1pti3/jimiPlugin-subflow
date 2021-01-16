import time
import copy

from core.models import action
from core import helpers, function, logging

from plugins.subflow.models import trigger as subflowTrigger

class _subflow(action._action):
	subflowName = str()
	subflowValue = str()
	
	def __init__(self):
		self.subflowExecuteTriggerCache = None

	def run(self,data,persistentData,actionResult):
		if not self.subflowExecuteTriggerCache:
			self.subflowExecuteTriggerCache = subflowTrigger._subflowExecute().getAsClass(query={ "subflowMatch.subflowName" : { "$in" : [ self.subflowName ] }, "subflowMatch.subflowValue" : { "$in" : [ self.subflowValue ] } })
		# Improve speed by checking if copy is needed - copy is used to prevent one flow modifying the data of another
		if len(self.subflowExecuteTriggerCache) > 1:
			passData = copy.deepcopy(data)
			for subflowExecuteTriggerCache in self.subflowExecuteTriggerCache:
				if not passData:
					passData = copy.deepcopy(data)
				subflowExecuteTriggerCache.notify(events=[passData["event"]],var=passData["var"],callingTriggerID=passData["triggerID"],persistentData=persistentData)
				passData = None
		elif len(self.subflowExecuteTriggerCache) == 1:
			subflowExecuteTriggerCache = self.subflowExecuteTriggerCache[0]
			subflowExecuteTriggerCache.notify(events=[data["event"]],var=data["var"],callingTriggerID=data["triggerID"],persistentData=persistentData)

		actionResult["result"] = True
		actionResult["rc"] = 0
		return actionResult
