import importlib
import os
import pkgutil

import yaml
from cachetools.func import lru_cache


class DevCliContext:

    def __init__(self, config) -> None:
        self.config = config

        self.load_plugins()

    def load_plugins(self):
        self.plugins = {
            name: importlib.import_module(name)
            for finder, name, ispkg
            in pkgutil.iter_modules()
            if name.startswith('devcli')
        }

    @lru_cache
    def get_plugin_scripts(self, script_name):
        print(self.plugins)
        return [getattr(plugin, script_name) for plugin in self.plugins.values() if hasattr(plugin, script_name)]

    def from_config_file():
        with open(os.path.join(os.getenv("HOME"), '.devcli_config')) as file:
            config = yaml.load(file)
            return DevCliContext(config)
