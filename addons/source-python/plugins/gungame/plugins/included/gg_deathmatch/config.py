# ../gungame/plugins/included/gg_deathmatch/config.py

"""Creates the gg_deathmatch configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Cvars
from cvars.flags import ConVarFlags

# GunGame Imports
#   Config
from gungame.core.config.manager import GunGameConfigManager

# Script Imports
from .info import info



# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as config:
    with config.cvar(
            'gg_deathmatch_delay', 2, ConVarFlags.NONE,
            'Set to the number of seconds to respawn ' +
            'players after the die.') as cvar:
        ...
