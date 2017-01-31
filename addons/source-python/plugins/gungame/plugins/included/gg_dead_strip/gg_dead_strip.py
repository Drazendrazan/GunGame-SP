# ../gungame/plugins/included/gg_dead_strip/gg_dead_strip.py

"""Plugin to strip weapons when a player dies."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events import Event
from filters.weapons import WeaponIter
from weapons.manager import weapon_manager

# GunGame
from gungame.core.status import GunGameMatchStatus, GunGameStatus


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_death')
def _strip_weapons(game_event):
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    for weapon in WeaponIter(
        not_filters=(
            tag for tag in ('tool', 'objective') if tag in weapon_manager.tags
        )
    ):
        if weapon.owner is None:
            weapon.remove()
