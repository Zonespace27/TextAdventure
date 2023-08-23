from ._component import Component
from base_obj import BaseObj
from physical_obj import PhysObj
from events.events import EVENT_INVENTORY_ADD_OBJECT, \
                        EVENT_INVENTORY_REMOVE_OBJECT, \
                        EVENT_INVENTORY_GET_CONTENTS, \
                        EVENT_RETVAL_BLOCK_INVENTORY_ADD, \
                        EVENT_OBJECT_ADDING_TO_INVENTORY, \
                        EVENT_RETVAL_BLOCK_OBJECT_INVENTORY_ADD, \
                        EVENT_RETVAL_BLOCK_INVENTORY_REMOVE, \
                        EVENT_OBJECT_ADDED_TO_INVENTORY, \
                        EVENT_OBJECT_REMOVING_FROM_INVENTORY, \
                        EVENT_OBJECT_REMOVED_FROM_INVENTORY, \
                        EVENT_RETVAL_BLOCK_OBJECT_INVENTORY_REMOVE
from events.verb_events import EVENT_VERB_CHECK_INVENTORY
from object import Object
from ..verbs._verb_names import VERB_CHECK_INVENTORY

class ComponentInventory(Component):
    id = "component_inventory"

    def __init__(self, args_dict = dict[str]) -> None:
        super().__init__()

        self.inventory: list[Object] = []

        # How many items can fit into this inventory
        self.inventory_size: int = self.arg_set(args_dict, "inventory_size", int)


    def attach_to_parent(self, object_to_attach: BaseObj) -> bool:
        if not isinstance(object_to_attach, PhysObj):
            return False
        
        object_to_attach: PhysObj

        if not super().attach_to_parent(object_to_attach):
            return False

        self.register_event(object_to_attach, EVENT_INVENTORY_ADD_OBJECT, self.on_attempt_object_add)
        self.register_event(object_to_attach, EVENT_INVENTORY_REMOVE_OBJECT, self.on_attempt_object_remove)
        self.register_event(object_to_attach, EVENT_INVENTORY_GET_CONTENTS, self.return_inventory_contents) # We commit a mild amount of sin
        self.register_event(object_to_attach, EVENT_VERB_CHECK_INVENTORY, self.check_inventory)
        object_to_attach.add_verb(VERB_CHECK_INVENTORY)
    

    def detach_from_parent(self):
        phys_parent: PhysObj = self.parent

        if phys_parent:
            self.unregister_event(phys_parent, EVENT_INVENTORY_ADD_OBJECT)
            self.unregister_event(phys_parent, EVENT_INVENTORY_REMOVE_OBJECT)
            self.unregister_event(phys_parent, EVENT_INVENTORY_GET_CONTENTS)
            self.unregister_event(phys_parent, EVENT_VERB_CHECK_INVENTORY)
            phys_parent.remove_verb(VERB_CHECK_INVENTORY)

        return super().detach_from_parent()
    

    def on_attempt_object_add(self, source, object_to_add: Object, silent: bool = False): #is any of this good practice?
        """
        ### EVENT FUNCT
        """

        if object_to_add in self.inventory:
            return EVENT_RETVAL_BLOCK_INVENTORY_ADD
        
        if len(self.inventory) >= self.inventory_size:
            return EVENT_RETVAL_BLOCK_INVENTORY_ADD

        if self.send_event(object_to_add, EVENT_OBJECT_ADDING_TO_INVENTORY, self.parent, self) == EVENT_RETVAL_BLOCK_OBJECT_INVENTORY_ADD: #unused currently
            return EVENT_RETVAL_BLOCK_INVENTORY_ADD
        
        if object_to_add.current_room:
            object_to_add.current_room.remove_from_contents(object_to_add)
        
        self.add_object(object_to_add, silent)
    
    
    def add_object(self, object_to_add: Object, silent: bool = False):
        physobj_parent: PhysObj = self.parent
        object_to_add.current_room = physobj_parent.current_room
        object_to_add.move_location(self)

        self.inventory.append(object_to_add)
        
        self.send_event(object_to_add, EVENT_OBJECT_ADDED_TO_INVENTORY, self.parent, self)

        if not silent:
            print(f"You pick up the {object_to_add.name}.")
    

    def on_attempt_object_remove(self, source, object_to_remove: Object, silent: bool = False):
        """
        ### EVENT FUNCT
        """

        if not (object_to_remove in self.inventory):
            return EVENT_RETVAL_BLOCK_INVENTORY_REMOVE

        if self.send_event(object_to_remove, EVENT_OBJECT_REMOVING_FROM_INVENTORY, self.parent, self) == EVENT_RETVAL_BLOCK_OBJECT_INVENTORY_REMOVE: #unused as well
            return EVENT_RETVAL_BLOCK_INVENTORY_REMOVE
        
        self.remove_object(object_to_remove, silent)
    

    def remove_object(self, object_to_remove: Object, silent: bool = False):
        physobj_parent: PhysObj = self.parent

        self.inventory.remove(object_to_remove)
        object_to_remove.current_room = physobj_parent.current_room
        object_to_remove.move_location(object_to_remove.current_room)

        object_to_remove.current_room.add_to_room(object_to_remove)
        
        self.send_event(object_to_remove, EVENT_OBJECT_REMOVED_FROM_INVENTORY, self.parent, self)

        if not silent:
            print(f"You drop the {object_to_remove.name}.")


    def check_inventory(self, source):
        """
        ### EVENT FUNCT
        """
        remaining_space = self.inventory_size - len(self.inventory)
        contents = "You currently have: \n"
        for index, inv_object in enumerate(self.inventory):
            contents += inv_object.name + ("\n" if (self.inventory[index] == self.inventory[len(self.inventory) - 1]) else ", ")

        contents += f"in your inventory, it looks like it could hold {remaining_space} more thing" + ("s." if remaining_space != 1 else ".")
        print(contents)
    

    def return_inventory_contents(self, source) -> list[Object]:
        """
        ### EVENT FUNCT
        """
        return self.inventory