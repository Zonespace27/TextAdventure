# From Room.add_to_room(), called on the physobj when it enters a room (entered_room<Room>)
EVENT_PHYSOBJ_ENTERED_ROOM = "physobj_entered_room"


# From Room.add_to_room(), called on all physobjects in a room when one enters the room. (entered_object<PhysObj>)
EVENT_ROOM_PHYSOBJ_ENTERED = "room_physobj_entered"


# From Player.find_nearby_objects_by_name() and Player.check_command(), called on all objects in a room and in the player's inventory, expected to return nothing or a list of contained (not in room) objects
EVENT_PLAYER_FIND_CONTENTS = "player_find_contents"


# From ComponentItem.attempt_pickup(), called on an object to add another object to the first one's inventory, should they have one (object_to_add<PhysObj>, silent<bool>)
# Return EVENT_RETVAL_BLOCK_INVENTORY_ADD to block the addition
EVENT_INVENTORY_ADD_OBJECT = "inventory_add_object"
EVENT_RETVAL_BLOCK_INVENTORY_ADD = (1 << 0)

# From ComponentItem.attempt_drop(), called on an object to drop an item from its inventory (object_to_remove<PhysObj>, silent<bool>)
# Return EVENT_RETVAL_BLOCK_INVENTORY_REMOVE to block the removal
EVENT_INVENTORY_REMOVE_OBJECT = "inventory_remove_object"
EVENT_RETVAL_BLOCK_INVENTORY_REMOVE = (1 << 0)

# From Player.find_nearby_objects_by_name(), called on an object to return a list of its inventory objects, should it have the component ()
EVENT_INVENTORY_GET_CONTENTS = "inventory_get_contents"

# From ComponentInventory.on_attempt_object_add(), called on an object when it is being added to an inventory. (inventory_owner<PhysObj>, inventory<ComponentInventory>)
# Return EVENT_RETVAL_BLOCK_INVENTORY_ADD to block the addition
EVENT_OBJECT_ADDING_TO_INVENTORY = "object_adding_to_inventory"
EVENT_RETVAL_BLOCK_OBJECT_INVENTORY_ADD = (1 << 0)

# From ComponentInventory.on_attempt_object_remove(), called on an object when it is being removed from an inventory. (inventory_owner<PhysObj>, inventory<ComponentInventory>)
# Return EVENT_RETVAL_BLOCK_INVENTORY_ADD to block the addition
EVENT_OBJECT_REMOVING_FROM_INVENTORY = "object_removing_from_inventory"
EVENT_RETVAL_BLOCK_OBJECT_INVENTORY_REMOVE = (1 << 0)


# From ComponentInventory.object_add(), called on an object when it has been added to an inventory. (inventory_owner<PhysObj>, inventory<ComponentInventory>)
EVENT_OBJECT_ADDED_TO_INVENTORY = "object_added_to_inventory"

# From ComponentInventory.object_remove(), called on an object when it has been added to an inventory. (inventory_owner<PhysObj>, inventory<ComponentInventory>)
EVENT_OBJECT_REMOVED_FROM_INVENTORY = "object_removed_from_inventory"


# From Player.look_around_room(), called on everything in a room when the player looks around, which counts the first entry, too ()
# Return EVENT_RETVAL_BLOCK_BASEOBJ_PRINT_DESCRIPTION to prevent that baseobj's desc from being printed
# Return EVENT_RETVAL_BLOCK_ALL_PRINT_DESCRIPTION (ONLY FROM THE ROOM, NOT OBJECTS) to prevent everything in the room from being printed, does block all the normally-ensuing EVENT_BASEOBJ_PRINT_DESCRIPTION events as well
EVENT_BASEOBJ_PRINT_DESCRIPTION = "baseobj_print_description"
EVENT_RETVAL_BLOCK_BASEOBJ_PRINT_DESCRIPTION = (1 << 0)
EVENT_RETVAL_BLOCK_ALL_PRINT_DESCRIPTION = (1 << 1)


# From PhysObj.location_move(), called on an object when it is moved to another location
EVENT_PHYSOBJ_LOCATION_MOVE = "physobj_location_move"


# From ComponentKey.attempt_unlock(), called on an object when an object with a key component is used on it (key_id<str>)
EVENT_LOCK_ATTEMPT_UNLOCK = "lock_attempt_unlock"

EVENT_DOOR_ATTEMPT_OPEN = "door_attempt_open"
EVENT_RETVAL_BLOCK_DOOR_OPEN = (1 << 0)

# Generic event to enable dialogue on an object, should it have a ComponentDialogue
EVENT_ENABLE_DIALOGUE = "enable_dialogue"

# Generic event to disable dialogue on an object, should it have a ComponentDialogue
EVENT_DISABLE_DIALOGUE = "disable_dialogue"

# Event that is called whenever dispose() is called on a baseobj
EVENT_BASEOBJ_DISPOSED = "baseobj_disposed"

# Event used for unit testing to confirm that events work as intended
EVENT_UNIT_TEST_SIGNAL = "unit_test_signal"
EVENT_RETVAL_UNIT_TEST_SIGNAL_RESPOND = (1 << 0)

# Second event used for unit testing
EVENT_UNIT_TEST_SIGNAL_2 = "unit_test_signal_2"

# Event called whenever a dialogue component finishes its dialogue
EVENT_DIALOGUE_COMPLETED = "dialogue_completed"
