import base_obj
import room

class PhysObj(base_obj.BaseObj):
    """
    Anything physical inside a room (not the room itself) should be a child of this.
    Player, object, item, person, etc.
    """
    
    def __init__(self) -> None:
        super().__init__()
        
        # If this Obj should be visually in a room
        self.player_visible = True
        # The current room loc of this Obj
        self.current_room: room.Room = None
    
    def move_rooms(self, new_room: room.Room):
        self.current_room.remove_from_room(self)
        new_room.add_to_room(self)