from base_obj import BaseObj

class Verb(BaseObj):
    """
    Verbs are singleton objects that are meant to be used to genericize actions that can be done to the object.
    """

    def __init__(self) -> None:
        super().__init__()

        # What strings will trigger the verb, such as "read"
        self.action_strings: list[str] = []
        # What args this is expecting
        self.expected_args: list[BaseObj] = []
        # Custom ID of this verb
        self.verb_id: str = "base"
        # If this verb should fail if not provided with the correct arg count
        self.requires_all_args: bool = True
    
    def action_string_is_valid(self, owning_obj: BaseObj, verb_string: str):
        if verb_string in self.action_strings:
            return True
        return False
    
    def argument_is_valid(self):
        pass


    def try_execute_verb(self, owning_obj: BaseObj, arguments: list[str] = []) -> bool:
        if self.requires_all_args and not (len(arguments) == len(self.expected_args)):
            return False
        
        self.execute_verb(owning_obj, arguments)
        return True
    

    def execute_verb(self, owning_obj: BaseObj, arguments: list[str] = []):
        pass