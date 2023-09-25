from plugin import BasePlugin

class Listener:
    def __init__(self):
        self.plugins = []

    def register_plugin(self, plugin: BasePlugin):
        self.plugins.append(plugin)

    def execute_plugins(self, model_response):
        for plugin in self.plugins:
            plugin.execute(model_response)
