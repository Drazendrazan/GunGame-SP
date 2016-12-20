# ../gungame/plugins/included/gg_teamplay/deathmatch.py

"""Deathmatch-based teamplay functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events import Event

# GunGame
from gungame.core.config.weapon import prop_physics
from gungame.core.players.dictionary import player_dictionary
from gungame.core.weapons.groups import grenade_weapons, melee_weapons

# Plugin
from .configuration import count_grenade_kills, count_melee_kills
from .manager import team_dictionary


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_death')
def _increment_team_multi_kill(game_event):
    attacker = player_dictionary.get(game_event['attacker'])
    if attacker is None:
        return

    victim = player_dictionary[game_event['userid']]
    if victim.team == attacker.team:
        return

    team = team_dictionary.get(attacker.team)
    if team is None:
        return

    weapon = game_event['weapon']
    if weapon != team.level_weapon:
        if weapon == 'prop_physics' and not prop_physics.get_int():
            return

        elif weapon in melee_weapons and not count_melee_kills.get_int():
            return

        elif weapon in grenade_weapons and not count_grenade_kills.get_int():
            return

    team.increase_multi_kill()
