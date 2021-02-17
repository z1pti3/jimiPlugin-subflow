import time
import copy

import jimi

from core.models import action
from core import helpers, function, logging

from plugins.subflow.models import trigger as subflowTrigger

class _subflow(action._action):
	subflowName = str()
	subflowValue = str()
	
	def __init__(self):
		self.subflowExecuteTriggerCache = None

	def doAction(self,data):
		if not self.subflowExecuteTriggerCache:
			self.subflowExecuteTriggerCache = subflowTrigger._subflowExecute().getAsClass(query={ "subflowMatch.subflowName" : { "$in" : [ self.subflowName ] }, "subflowMatch.subflowValue" : { "$in" : [ self.subflowValue ] } })
		data["flowData"]["calling_trigger_id"] = data["flowData"]["trigger_id"]
		# Improve speed by checking if copy is needed - copy is used to prevent one flow modifying the data of another
		if len(self.subflowExecuteTriggerCache) > 1:
			tempData = jimi.conduct.copyData(data)
			for subflowExecuteTriggerCache in self.subflowExecuteTriggerCache:
				if not tempData:
					tempData = jimi.conduct.copyData(data)
				subflowExecuteTriggerCache.notify(events=[tempData["flowData"]["event"]],data=tempData)
				tempData = None
		elif len(self.subflowExecuteTriggerCache) == 1:
			subflowExecuteTriggerCache = self.subflowExecuteTriggerCache[0]
			subflowExecuteTriggerCache.notify(events=[data["flowData"]["event"]],data=data)

		return { "result" : True, "rc" : 0 }
