from ._component import Component
from base_obj import BaseObj
from player import Player
from events.verb_events import EVENT_VERB_GET_UP, EVENT_VERB_TRY_EXECUTE, EVENT_RETVAL_BLOCK_VERB_EXECUTE
from ..verbs._verb_names import VERB_GET_UP
from ..verbs._verb import Verb
import globals
from bitflags import VERB_IGNORE_SITDOWN

class ComponentSittingDown(Component):
    id = "component_sitting_down"

    def __init__(self, args_dict = dict[str]) -> None:
        super().__init__()

        # What message is given when you get up
        self.get_up_message = self.arg_set(args_dict, "get_up_message", str) or "You get up from the chair."


    def attach_to_parent(self, object_to_attach: BaseObj) -> bool:
        if not isinstance(object_to_attach, Player):
            return False
        
        object_to_attach: Player

        if not super().attach_to_parent(object_to_attach):
            return False

        object_to_attach.add_verb(VERB_GET_UP)
        self.register_event(object_to_attach, EVENT_VERB_GET_UP, self.get_up)
        self.register_event(object_to_attach, EVENT_VERB_TRY_EXECUTE, self.on_verb_execute)


    def detach_from_parent(self):
        player_parent: Player = self.parent

        if player_parent:
            player_parent.remove_verb(VERB_GET_UP)
            self.unregister_event(player_parent, EVENT_VERB_GET_UP)
            self.unregister_event(player_parent, EVENT_VERB_TRY_EXECUTE)

        return super().detach_from_parent()

    
    def get_up(self, source):
        """
        ### EVENT FUNCT
        """
        print(self.get_up_message) #TODO: make this work for sitting down in a chair #TODO: check if this TODO is valid
        globals.qdel(self)

    
    def on_verb_execute(self, source, executing_verb: Verb, owning_obj: BaseObj):
        """
        ### EVENT FUNCT
        """
        if(executing_verb.verb_flags & VERB_IGNORE_SITDOWN):
            return
        print("You can't do this while sitting down!")
        return EVENT_RETVAL_BLOCK_VERB_EXECUTE
