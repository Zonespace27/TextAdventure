from typing import TYPE_CHECKING
from base_obj import BaseObj
import globals

if TYPE_CHECKING:
    import room
    from packages.verbs._verb import Verb


class PhysObj(BaseObj):
    """
    Anything physical inside a room (not the room itself) should be a child of this.
    Player, object, item, person, etc.
    """

    json_location: str = 'textadventure/json/phys_objects.json'
    
    def __init__(self, object_id: str = "") -> None:
        super().__init__(object_id)

        # The _primary_ name something will be referred to as
        self.name: str = ""
        # A list of all names that work for this, self.name is appended as well
        self.alternate_names: list[str] = []
        # A general, light description of this obj
        self.desc: str = ""
        
        # The current room loc of this Obj
        self.current_room: "room.Room" = None
        # If this object is in some form of inventory, instead of being directly in a room or such
        self.in_inventory = False
        # This object's location (e.g. an inventory component or a room)
        self.location: BaseObj = None

        if object_id:
            self.name = globals.object_id_data[object_id]["name"]
            self.alternate_names = globals.object_id_data[object_id]["alternate_names"].copy()
            self.desc = globals.object_id_data[object_id]["desc"]
        
        self.alternate_names.append(self.name)
    

    def dispose(self):
        if self.current_room:
            self.current_room.remove_from_room(self, True)
        return super().dispose()

    
    def move_rooms(self, new_room: "room.Room"):
        self.current_room.remove_from_room(self)
        new_room.add_to_room(self)
    

    def action_is_valid(self, action_string: str) -> "Verb":
        for verb in self.source_verbs:
            if verb.action_string_is_valid(self, action_string):
                return verb
        return None
    

    def name_is_valid(self, name_to_try: str) -> bool:
        """
        A method used to check if a proposed name is valid for this physical object
        """
        if name_to_try.lower() in self.alternate_names:
            return True
        return False