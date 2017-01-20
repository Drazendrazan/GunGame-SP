# ../gungame/plugins/included/gg_multi_level/gg_multi_level.py

"""Plugin that allows players to gain special powers when multi-leveling."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from entities.entity import Entity
from events import Event
from filters.players import PlayerIter
from listeners import OnLevelEnd, on_tick_listener_manager
from listeners.tick import Delay
from mathlib import Vector
from players.entity import Player

# GunGame
from gungame.core.players.attributes import player_attributes
from gungame.core.players.dictionary import player_dictionary
from gungame.core.sounds.manager import sound_manager
from gungame.core.status import GunGameRoundStatus, GunGameStatus

# Plugin
from .configuration import (
    gravity, levels, speed, tk_attacker_reset, tk_victim_reset,
)
from .custom_events import GG_Multi_Level


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    player_attributes.register_attribute('multi_levels', 0)


def unload():
    player_attributes.unregister_attribute('multi_levels')


# =============================================================================
# >> CLASSES
# =============================================================================
class _MultiLevelPlayer(Player):
    """"""

    spark_entity = None
    delay = None

    def __init__(self, index):
        super(_MultiLevelPlayer, self).__init__(index)
        self.sound = sound_manager.emit_sound('multi_level', index)
        self.start_gravity = self.gravity
        self.start_speed = self.speed
        self.gravity = gravity.get_int() / 100
        self.speed = speed.get_int() / 100
        self.give_spark_entity()
        self.delay = Delay(
            delay=self.sound.duration,
            callback=multi_level_manager.__delitem__,
            args=(self.userid, ),
        )

    def give_spark_entity(self):
        entity = self.spark_entity = Entity.create('env_spark')
        entity.spawn_flags = 896
        entity.angles = Vector(-90, 0, 0)
        entity.magnitude = 8
        entity.trail_length = 3
        entity.set_parent(self, -1)
        entity.origin = self.origin
        entity.start_spark()

    def remove_multi_level(self):
        if self.delay is not None and self.delay.running:
            self.delay.cancel()
        self.delay = None
        self.gravity = self.start_gravity
        self.speed = self.start_speed
        self.sound.stop(self.index)
        self.remove_spark_entity()

    def remove_spark_entity(self):
        self.spark_entity.stop_spark()
        self.spark_entity.remove()


class _MultiLevelManager(dict):
    """"""

    def __delitem__(self, userid, reset_levels=True):
        if reset_levels:
            player_dictionary[userid].multi_levels = 0
        if userid not in self:
            return
        self[userid].remove_multi_level()
        super(_MultiLevelManager, self).__delitem__(userid)
        if not len(self):
            on_tick_listener_manager.unregister_listener(self._tick)

    def clear(self, silent=False):
        if silent:
            super().clear()
            return
        for userid in list(self):
            del self[userid]

    def delete_disconnecting_player(self, userid):
        self.__delitem__(userid, reset_levels=False)

    def give_multi_level(self, userid):
        if not len(self):
            on_tick_listener_manager.register_listener(self._tick)
        if userid in self:
            self.__delitem__(userid, reset_levels=False)
        self[userid] = _MultiLevelPlayer.from_userid(userid)
        with GG_Multi_Level() as event:
            event.userid = userid
            event.leveler = userid

    def _tick(self):
        current_gravity = gravity.get_int()
        for player in self.values():
            player.gravity = current_gravity

multi_level_manager = _MultiLevelManager()


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event('gg_level_up')
def _player_level_up(game_event):
    if GunGameStatus.ROUND != GunGameRoundStatus.ACTIVE:
        return
    player = player_dictionary[game_event['leveler']]
    old = player.multi_levels
    player.multi_levels += 1
    if player.multi_levels >= levels.get_int():
        # Give or increase multi-level
        multi_level_manager.give_multi_level(player.userid)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_death')
def _reset_team_killers(game_event):
    userid = game_event['userid']
    attacker = game_event['attacker']

    # Suicide?
    if attacker in (0, userid):
        del multi_level_manager[userid]
        return

    # Not team-kill?
    if Player.from_userid(userid).team != Player.from_userid(attacker).team:
        del multi_level_manager[userid]
        return

    # Reset team-kill victim's multi-level?
    if not tk_victim_reset.get_bool():
        del multi_level_manager[userid]

    # Reset the team-killer's multi-level?
    if tk_attacker_reset.get_bool():
        del multi_level_manager[attacker]


@Event('player_disconnect')
def _remove_disconnecting_player(game_event):
    multi_level_manager.delete_disconnecting_player(game_event['userid'])


@Event('round_end')
def _reset_multi_level(game_event):
    multi_level_manager.clear()
    for player in PlayerIter():
        player_dictionary[player.userid].multi_levels = 0


# =============================================================================
# >> LISTENERS
# =============================================================================
@OnLevelEnd
def _clear_multi_level():
    multi_level_manager.clear(silent=True)
