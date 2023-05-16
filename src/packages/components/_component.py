from base_obj import BaseObj
from globals import qdel

class Component(BaseObj):
    """
    A way to add generic functionality (e.g. edibility) without needing to make a subtype for that specifically.
    Components should ideally not have functions be manually called by the parent, instead relying on events to make things happen.
    """
    # The string ID of this component
    id: str = ""

    def __init__(self, args_dict = dict[str]) -> None:
        super().__init__()

        # The owner of this component
        self.parent: BaseObj = None
    

    def dispose(self):
        self.detach_from_parent()
        return super().dispose()

    
    def attempt_attachment(self, object_to_attach: BaseObj):
        if self.__class__ in object_to_attach.object_components:
            qdel(object_to_attach.object_components[self.__class__])
        
        self.attach_to_parent(object_to_attach)


    def attach_to_parent(self, object_to_attach: BaseObj) -> bool: # TODO: Test this shit
        object_to_attach.object_components[self.__class__] = self
        self.parent = object_to_attach
        return True

    
    def detach_from_parent(self):
        self.parent = None


    def arg_set(self, dict_to_use: dict[str], key_name: str, return_int: bool = False): # 3rd arg is a little gross but i'll live w/ it for now
        """
        Used as part of setting a component's argument from a passed in dict
        """
        if key_name not in list(dict_to_use.keys()):
            return (0 if return_int else "")

        return dict_to_use[key_name]
