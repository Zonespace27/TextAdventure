from ._component import Component
from base_obj import BaseObj
from physical_obj import PhysObj
from events.events import EVENT_BASEOBJ_PRINT_DESCRIPTION, EVENT_RETVAL_BLOCK_BASEOBJ_PRINT_DESCRIPTION, EVENT_PLAYER_FIND_CONTENTS
from events.verb_events import EVENT_VERB_OPEN_CONTAINER, EVENT_VERB_CLOSE_CONTAINER, EVENT_VERB_EXAMINE
from object import Object
from ..verbs._verb_names import VERB_OPEN_CONTAINER, VERB_EXAMINE
from traits import TRAIT_LOCKED

class ComponentContainer(Component):
    id = "component_container"

    def __init__(self, args_dict = dict[str]) -> None:
        super().__init__()

        self.contents: list[Object] = []

        # If the container is open or closed
        self.open = self.arg_set(args_dict, "open", bool)
        # If the container needs to bother with being open or closed at all
        self.requires_open = self.arg_set(args_dict, "requires_open", bool)
        # If the container should visibly be open or closed
        self.open_visibility = self.arg_set(args_dict, "open_visibility", bool)
        # If the container should ever show its contents on examine
        self.show_contents_examine = self.arg_set(args_dict, "show_contents_examine", bool)
        # Message shown to the user when they open the container
        self.open_message = self.arg_set(args_dict, "open_message", str) or "You open the container."
        # Message shown to the user when they close the container
        self.close_message = self.arg_set(args_dict, "close_message", str) or "You close the container."
        # Message shown to the user when they examine the container, if it doesn't have an open/closed state
        self.no_open_close_examine_message = self.arg_set(args_dict, "no_open_close_examine_message", str) or "You look closer at the container."
        # Message shown to the user when they examine the container when it is open
        self.open_examine_message = self.arg_set(args_dict, "open_examine_message", str) or "You look closer at the container. Inside, you see:\n"
        # Message shown to the user when they examine the container when it is closed
        self.closed_examine_message = self.arg_set(args_dict, "closed_examine_message", str) or "You look closer at the container."     

        self.set_initial_contents(self.arg_set(args_dict, "initial_contents", list))


    def attach_to_parent(self, object_to_attach: BaseObj) -> bool:
        if not isinstance(object_to_attach, PhysObj):
            return False
        
        object_to_attach: PhysObj

        self.register_event(object_to_attach, EVENT_VERB_OPEN_CONTAINER, self.open_container)
        self.register_event(object_to_attach, EVENT_VERB_CLOSE_CONTAINER, self.close_container)
        self.register_event(object_to_attach, EVENT_BASEOBJ_PRINT_DESCRIPTION, self.on_view)
        self.register_event(object_to_attach, EVENT_PLAYER_FIND_CONTENTS, self.get_contents)
        self.register_event(object_to_attach, EVENT_VERB_EXAMINE, self.on_examine)
        object_to_attach.add_verb(VERB_OPEN_CONTAINER)
        object_to_attach.add_verb(VERB_EXAMINE)

        return super().attach_to_parent(object_to_attach)
    

    def detach_from_parent(self):
        phys_parent: PhysObj = self.parent

        if phys_parent:
            self.unregister_event(phys_parent, EVENT_VERB_OPEN_CONTAINER)
            self.unregister_event(phys_parent, EVENT_VERB_CLOSE_CONTAINER)
            self.unregister_event(phys_parent, EVENT_BASEOBJ_PRINT_DESCRIPTION)
            self.unregister_event(phys_parent, EVENT_PLAYER_FIND_CONTENTS)
            self.unregister_event(phys_parent, EVENT_VERB_EXAMINE)
            self.remove_verb(VERB_OPEN_CONTAINER)
            self.remove_verb(VERB_EXAMINE)

        return super().detach_from_parent()
    

    def set_initial_contents(self, content_list: list[str]):
        for entry in content_list:
            self.add_object(Object(entry))
    

    def add_object(self, object: Object, silent: bool = False):
        self.contents.append(object)
        object.move_location(self.parent)
    
    
    def remove_object(self, object: Object, silent: bool = False):
        self.contents.remove(object)
    

    def open_container(self, source):
        """
        ### EVENT FUNCT
        """
        if self.open or (not self.requires_open):
            return
        
        if self.parent.has_trait(TRAIT_LOCKED):
            print("You can't open this, it's locked!")
            return

        self.open = True
        print(self.open_message)


    def close_container(self, source):
        """
        ### EVENT FUNCT
        """
        if (not self.open) or (not self.requires_open):
            return

        self.open = False
        print(self.close_message)
    
    
    def on_view(self, source) -> str:
        """
        ### EVENT FUNCT
        """
        if not self.requires_open:
            return

        phys_parent: PhysObj = self.parent
        open_or_close_string: str = "It is " + ("open." if self.open else "closed.")

        print(f"{phys_parent.desc} {open_or_close_string}")
        return EVENT_RETVAL_BLOCK_BASEOBJ_PRINT_DESCRIPTION


    def get_contents(self, source) -> list[Object]:
        """
        ### EVENT FUNCT
        """
        if not self.requires_open:
            return self.contents

        return (self.contents if self.open else [])
    

    def on_examine(self, source):
        """
        ### EVENT FUNCT
        """
        if not self.requires_open:
            print(self.no_open_close_examine_message)
            if self.show_contents_examine:
                content_objects: str = ""
                for index, object in enumerate(self.contents):
                    content_objects += (object.name + (", " if index != (len(self.contents) - 1) else "."))
                print(content_objects)
            return

        if self.open:
            print(self.open_examine_message)
            if self.show_contents_examine:
                content_objects: str = ""
                for index, object in enumerate(self.contents):
                    content_objects += (object.name + (", " if index != (len(self.contents) - 1) else "."))
                print(content_objects)
        else:
            print(self.closed_examine_message)