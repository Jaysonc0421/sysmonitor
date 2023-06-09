import inspect
import os
import importlib

class PluginManager:
    def __init__(self, plugins_dir, doc_ref):
        self.plugins_dir = plugins_dir
        self.doc_ref = doc_ref
        self.plugins = {}

    def load_plugins(self):
        plugin_files = [file for file in os.listdir(self.plugins_dir) if file.endswith('.py')]
        for plugin_file in plugin_files:
            module_name = os.path.splitext(plugin_file)[0]
            module = importlib.import_module(f'plugins.{module_name}')
            plugin_class = self.find_plugin_class(module)
            if plugin_class:
                plugin = plugin_class(self.doc_ref)
                self.plugins[module_name] = plugin
        print('Plugins loaded: ' + ', '.join(list(self.plugins)))

    def find_plugin_class(self, module):
        for name, obj in module.__dict__.items():
            if inspect.isclass(obj):
                return obj
        return None
