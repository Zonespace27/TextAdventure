import object
import physical_obj
import events
import base_obj as base_obj
import globals

class Room(base_obj.BaseObj):

    def __init__(self, room_id: str, room_desc: str, room_objects: list[str], room_verbs: list[str]) -> None:
        super().__init__()

        self.id = room_id
        self.desc = room_desc

        self.contents: list[physical_obj.PhysObj] = []
        self.verbs = {}
        for obj in room_objects:
            self.add_to_room(object.Object(obj)) # TODO: Extend this to items and etc #TODO2: Check if calling the add proc might mess things up
        #TODO: Add verb implementation

        globals.roomid_to_room[room_id] = self
    
    def add_to_room(self, physobj_to_add: physical_obj.PhysObj):
        for obj in self.contents:
            physobj_to_add.send_event(obj, events.EVENT_ROOM_PHYSOBJ_ENTERED, self)
    
        self.contents.append(physobj_to_add)
        physobj_to_add.current_room = self

        self.send_event(physobj_to_add, events.EVENT_PHYSOBJ_ENTERED_ROOM, self)
    
    def remove_from_room(self, physobj_to_remove: physical_obj.PhysObj, deleted: bool = False):
        self.contents.remove(physobj_to_remove)
        physobj_to_remove.current_room = None