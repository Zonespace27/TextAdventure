from base_obj import BaseObj


class Element(BaseObj):
    """
    A less complex form of component, Elements are used as a lightweight form of component that cannot store data and is a singleton across all objects using that element.
    """
    # The string ID of this element
    id: str = ""

    def hook_object(self, object_to_hook: BaseObj) -> bool:
        return True

    def unhook_object(self, object_to_unhook: BaseObj) -> bool:
        return True
