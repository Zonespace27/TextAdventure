from base_obj import BaseObj
from events.verb_events import EVENT_VERB_CHECK_INVENTORY
from ._verb import Verb 
from ._verb_names import VERB_CHECK_INVENTORY

class VerbCheckInventory(Verb):
    verb_id = VERB_CHECK_INVENTORY

    def __init__(self) -> None:
        super().__init__()
        self.expected_args = []
        self.action_strings = [
            "check inventory",
            "check backpack",
            "look backpack",
            "look_inventory"
        ]
    

    def can_execute_verb(self, owning_obj: BaseObj, arguments: list = []) -> bool:
        if len(arguments) < len(self.expected_args):
            return False
        
        return super().can_execute_verb(owning_obj, arguments)
        

    def execute_verb(self, owning_obj: BaseObj, arguments: list = []):
        self.send_event(owning_obj, EVENT_VERB_CHECK_INVENTORY)