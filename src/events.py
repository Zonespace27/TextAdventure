# From Room.add_to_room(), called on the physobj when it enters a room (entered_room<Room>)
EVENT_PHYSOBJ_ENTERED_ROOM = "physobj_entered_room"


# From Room.add_to_room(), called on all physobjects in a room when one enters the room. (entered_object<PhysObj>)
EVENT_ROOM_PHYSOBJ_ENTERED = "room_physobj_entered"


# From VerbEat.execute_verb(), called on an object when the eat verb succeeds on it (eaten)
EVENT_VERB_EAT = "verb_eat"