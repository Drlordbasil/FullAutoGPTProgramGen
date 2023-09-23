class PluginManager:
    PLUGIN_DIR = "plugins"
    def __init__(self):
        if not os.path.exists(self.PLUGIN_DIR):
            os.makedirs(self.PLUGIN_DIR)
    def load_all_plugins(self):
        for plugin_name in os.listdir(self.PLUGIN_DIR):
            if plugin_name.endswith('.py'):
                self.load_plugin(plugin_name[:-3])
    def load_plugin(self, plugin_name):
        plugin_path = os.path.join(self.PLUGIN_DIR, f"{plugin_name}.py")
        if os.path.exists(plugin_path):
            with open(plugin_path, 'r') as f:
                code = f.read()
                exec(code, globals())
