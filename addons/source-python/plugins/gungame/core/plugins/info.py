# ../gungame/core/plugins/info.py

"""Provides a class to store sub-plugin info."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Site-package
from configobj import ConfigObj

# Source.Python
from plugins.info import PluginInfo

# GunGame
from ..paths import GUNGAME_PLUGINS_PATH


# =============================================================================
# >> CLASSES
# =============================================================================
class GunGamePluginInfo(PluginInfo):
    """Class used to store plugin info for GunGame sub-plugins."""

    def __init__(self, module):
        """Override __init__ to get the proper info."""
        path = module.split('.')
        if (
            not module.startswith('gungame.plugins.') or
            path[2] not in ('included', 'custom') or
            len(path) != 5
        ):
            raise ValueError(
                'Invalid plugin path given: {module}'.format(module=module)
            )
        name = path[3]
        ini_file = GUNGAME_PLUGINS_PATH / path[2] / name / 'info.ini'
        if not ini_file.isfile():
            raise ValueError(
                'No info.ini file found for plugin {name}'.format(name=name)
            )
        ini = ConfigObj(ini_file)
        super().__init__(name, **ini)
