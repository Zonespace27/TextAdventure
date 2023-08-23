import object
import physical_obj
import events
import base_obj as base_obj
import globals

class Room(base_obj.BaseObj):

    def __init__(self, room_id: str, room_desc: str, room_objects: list[str] = [], room_verbs: list[str] = [], room_components: dict[str, dict[str]] = {}, room_elements: list[str] = []) -> None:
        super().__init__()

        self.id = room_id
        self.desc = room_desc

        self.contents: list[physical_obj.PhysObj] = []
        self.verbs = {}
        for obj in room_objects:
            self.add_to_room(object.Object(obj))

        for verb in room_verbs:
            self.add_verb(verb)

        for component in list(room_components.keys()):
            self.add_component(globals.component_id_to_class[component], room_components[component])
        
        for element in room_elements:
            self.add_element(element)

        globals.roomid_to_room[room_id] = self
    
    def add_to_room(self, physobj_to_add: physical_obj.PhysObj):
        for obj in self.contents:
            physobj_to_add.send_event(obj, events.EVENT_ROOM_PHYSOBJ_ENTERED, self)
    
        self.contents.append(physobj_to_add)
        physobj_to_add.current_room = self
        physobj_to_add.location = self # This one is explicitly not using the location_move function

        self.send_event(physobj_to_add, events.EVENT_PHYSOBJ_ENTERED_ROOM, self)
    
    def remove_from_room(self, physobj_to_remove: physical_obj.PhysObj, deleted: bool = False):
        self.contents.remove(physobj_to_remove)
        physobj_to_remove.current_room = None
    
    def remove_from_contents(self, physobj_to_remove: physical_obj.PhysObj):
        """
        A method that removes an object from a room's contents without nulling out its current room. \n
        Useful for things like an object being in an inventory.
        """
        self.contents.remove(physobj_to_remove)
