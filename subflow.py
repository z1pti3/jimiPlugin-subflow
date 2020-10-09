from core import plugin, model

class _subflow(plugin._plugin):
    version = 0.1

    def install(self):
        # Register models
        model.registerModel("subflow","_subflow","_action","plugins.subflow.models.action")
        model.registerModel("subflowExecute","_subflowExecute","_trigger","plugins.subflow.models.trigger")
        return True

    def uninstall(self):
        # deregister models
        model.deregisterModel("subflow","_subflow","_action","plugins.subflow.models.action")
        model.deregisterModel("subflowExecute","_subflowExecute","_trigger","plugins.subflow.models.trigger")
        return True
    
    def upgrade(self,LatestPluginVersion):
        pass
    