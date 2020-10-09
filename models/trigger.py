from core.models import trigger, webui

class _subflowExecute(trigger._trigger):
    subflowMatch = list() # [{ "tagName" : str(), "tagValue" : str() }]

    class _properties(webui._properties):
        def generate(self,classObject):
            formData = []
            formData.append({"type" : "input", "schemaitem" : "name", "textbox" : classObject.name})
            formData.append({"type" : "json-input", "schemaitem" : "subflowMatch", "textbox" : classObject.subflowMatch})
            formData.append({"type" : "checkbox", "schemaitem" : "enabled", "checked" : classObject.enabled})
            formData.append({"type" : "json-input", "schemaitem" : "varDefinitions", "textbox" : classObject.varDefinitions})
            formData.append({"type" : "input", "schemaitem" : "logicString", "textbox" : classObject.logicString})
            return formData

