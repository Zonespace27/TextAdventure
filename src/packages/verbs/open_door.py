from physical_obj import PhysObj
from base_obj import BaseObj
from events import EVENT_VERB_OPEN_DOOR
from ._verb import Verb
from ._verb_names import VERB_OPEN_DOOR

class VerbOpenDoor(Verb):
    verb_id = VERB_OPEN_DOOR

    def __init__(self) -> None:
        super().__init__()
        self.expected_args = [ 
            PhysObj,
        ]
        self.action_strings = [
            "open",
            "walk into",
        ]
    

    def try_execute_verb(self, owning_obj: BaseObj, arguments: list[str] = []) -> bool:
        if len(arguments) < len(self.expected_args):
            return False
        
        # Add a signal to block it here

        return super().try_execute_verb(owning_obj, arguments)
        

    def execute_verb(self, owning_obj: BaseObj, arguments: list[str] = []):
        self.send_event(owning_obj, EVENT_VERB_OPEN_DOOR)
    
    
    #def argument_is_valid(self, argument: PhysObj, index):
    #    return super().argument_is_valid(argument, index)