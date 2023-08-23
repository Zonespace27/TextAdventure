from base_obj import BaseObj
from events.verb_events import EVENT_VERB_CAN_EXECUTE, EVENT_RETVAL_BLOCK_VERB_EXECUTE

class Verb(BaseObj):
    """
    Verbs are singleton objects that are meant to be used to genericize actions that can be done to the object.
    """
    # Custom ID of this verb
    verb_id: str = "base"

    def __init__(self) -> None:
        super().__init__()

        # What strings will trigger the verb, such as "read"
        self.action_strings: list[str] = []
        # What args this is expecting
        self.expected_args: list[BaseObj] = []
        # If this verb should fail if not provided with the correct arg count
        self.requires_all_args: bool = True
        # Bitflags for various verb things that don't need their own variable
        self.verb_flags = 0
    
    def action_string_is_valid(self, owning_obj: BaseObj, verb_string: str):
        if verb_string in self.action_strings:
            return True
        return False
    

    def argument_is_valid(self, argument, index):
        return True
    

    def can_execute_verb(self, owning_obj: BaseObj, arguments: list = []) -> bool:
        if self.requires_all_args and not (len(arguments) == len(self.expected_args)):
            return False
        
        if self.send_event(owning_obj, EVENT_VERB_CAN_EXECUTE, self) & EVENT_RETVAL_BLOCK_VERB_EXECUTE:
            return False
        
        return True
    

    def try_execute_verb(self, owning_obj: BaseObj, arguments: list = []) -> bool:
        if not self.can_execute_verb(owning_obj, arguments):
            return False
        
        self.execute_verb(owning_obj, arguments)
        return True
    

    def execute_verb(self, owning_obj: BaseObj, arguments: list = []):
        return


    def can_attach_to(self, object_to_attach: BaseObj):
        """
        Function to decide if this verb can be attached to object_to_attach.
        """
        return True