from ._component import Component
from base_obj import BaseObj
from player import Player
from events.verb_events import EVENT_VERB_GET_UP, EVENT_VERB_CAN_EXECUTE, EVENT_RETVAL_BLOCK_VERB_EXECUTE
from ..verbs._verb_names import VERB_GET_UP
from ..verbs._verb import Verb
import globals
from typing import TYPE_CHECKING
from bitflags import VERB_IGNORE_LAYDOWN, PLAYER_LAYING_DOWN

class ComponentLayingDown(Component):
    id = "component_laying_down"

    def __init__(self, args_dict = dict[str]) -> None:
        super().__init__()

        # What message is given when you get up
        self.get_up_message = self.arg_set(args_dict, "get_up_message", str) or "You get up from the floor."


    def attach_to_parent(self, object_to_attach: BaseObj) -> bool:
        if not isinstance(object_to_attach, Player):
            return False
        
        object_to_attach: Player

        if not super().attach_to_parent(object_to_attach):
            return False

        object_to_attach.add_verb(VERB_GET_UP)
        self.register_event(object_to_attach, EVENT_VERB_GET_UP, self.get_up)
        self.register_event(object_to_attach, EVENT_VERB_CAN_EXECUTE, self.on_verb_execute)
        object_to_attach.player_flags |= PLAYER_LAYING_DOWN


    def detach_from_parent(self):
        player_parent: Player = self.parent

        if player_parent:
            player_parent.remove_verb(VERB_GET_UP)
            self.unregister_event(player_parent, EVENT_VERB_GET_UP)
            self.unregister_event(player_parent, EVENT_VERB_CAN_EXECUTE)
            player_parent.player_flags &= ~PLAYER_LAYING_DOWN

        return super().detach_from_parent()

    
    def get_up(self, source):
        """
        ### EVENT FUNCT
        """
        print(self.get_up_message)
        globals.qdel(self)

    
    def on_verb_execute(self, source, executing_verb: Verb):
        """
        ### EVENT FUNCT
        """
        if(executing_verb.verb_flags & VERB_IGNORE_LAYDOWN):
            return
        print("You can't do this while lying down!")
        return EVENT_RETVAL_BLOCK_VERB_EXECUTE
