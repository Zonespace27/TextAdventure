from base_obj import BaseObj
from physical_obj import PhysObj
from events.verb_events import EVENT_VERB_EXAMINE
from ._verb import Verb 
from ._verb_names import VERB_EXAMINE

class VerbExamine(Verb):
    verb_id = VERB_EXAMINE

    def __init__(self) -> None:
        super().__init__()
        self.expected_args = [
            PhysObj,
        ]
        self.action_strings = [
            "examine",
            "view",
        ]
    

    def can_execute_verb(self, owning_obj: BaseObj, arguments: list = []) -> bool:
        if len(arguments) < len(self.expected_args):
            return False
        
        if not self.check_object_argument(owning_obj, arguments, 0):
            return False

        return super().can_execute_verb(owning_obj, arguments)
        

    def execute_verb(self, owning_obj: BaseObj, arguments: list = []):
        self.send_event(owning_obj, EVENT_VERB_EXAMINE)