# ../gungame/plugins/included/gg_earn_nade/configuration.py

"""Creates the gg_earn_nade configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.config.manager import GunGameConfigManager

# Plugin
from .info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'auto_switch_default',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:

    with _config.cvar('auto_switch_default') as auto_switch_default:
        auto_switch_default.add_text()
