from base_obj import BaseObj
from player import Player
from ._verb import Verb 
from ._verb_names import VERB_LOOK_AROUND

class VerbLookAround(Verb):
    verb_id = VERB_LOOK_AROUND

    def __init__(self) -> None:
        super().__init__()
        self.expected_args = []
        self.action_strings = [
            "look around",
            "look room",
            "check room",
        ]
    

    def try_execute_verb(self, owning_obj: Player, arguments: list[str] = []) -> bool:
        if not owning_obj.current_room: # Somehow?????
            return False

        return super().try_execute_verb(owning_obj, arguments)
        

    def execute_verb(self, owning_obj: Player, arguments: list[str] = []):
        owning_obj.look_around_room()
    

    def can_attach_to(self, object_to_attach: BaseObj):
        if not isinstance(object_to_attach, Player):
            return False
        return super().can_attach_to(object_to_attach)