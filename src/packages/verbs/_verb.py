from base_obj import BaseObj
from physical_obj import PhysObj
from events.verb_events import EVENT_VERB_TRY_EXECUTE, EVENT_RETVAL_BLOCK_VERB_EXECUTE
import globals

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
        
        """for argument in arguments:
            if not isinstance(argument, list):
                continue
            
            selection_string = "Which one? ARG (by number)\n"
            element_number_dict: dict[int, str] = {}
            element_number = 1
            for item in argument:
                item: PhysObj # TODO: make sure that verb args can only be physobjs
                element_number_dict[element_number] = item
                selection_string += f"({element_number}) {item.name}\n"
                element_number += 1

            while True:
                picked_number = input(selection_string)

                if not picked_number.isnumeric():
                    continue

                picked_number = int(picked_number)

                try:
                    list(element_number_dict.keys()).index(picked_number)
                
                except ValueError:
                    continue

                arguments[arguments.index(argument)] = element_number_dict[picked_number] # TODO: test this works
                break"""
        
        return True
    
    def check_object_argument(self, owning_obj: BaseObj, arguments: list = [], argument_index: int = 0) -> bool:
        """
        A method used where, given an object, list, and index, will check if the item in list[index] is the object, or is a list with the object inside it
        """
        if (len(arguments) - 1) < argument_index:
            return False
        
        if isinstance(arguments[argument_index], list):
            if owning_obj in arguments[argument_index]:
                return True
        
        else:
            if owning_obj == arguments[argument_index]:
                return True
        
        return False

    def try_execute_verb(self, owning_obj: BaseObj, arguments: list = []) -> bool: # Might be deprecated.
        #if not self.can_execute_verb(owning_obj, arguments):
        #    return False
        if self.send_event(globals.player_ref, EVENT_VERB_TRY_EXECUTE, self, owning_obj) & EVENT_RETVAL_BLOCK_VERB_EXECUTE:
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