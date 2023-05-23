# From Room.add_to_room(), called on the physobj when it enters a room (entered_room<Room>)
EVENT_PHYSOBJ_ENTERED_ROOM = "physobj_entered_room"


# From Room.add_to_room(), called on all physobjects in a room when one enters the room. (entered_object<PhysObj>)
EVENT_ROOM_PHYSOBJ_ENTERED = "room_physobj_entered"


# From VerbEat.execute_verb(), called on an object when the eat verb succeeds on it (eaten)
EVENT_VERB_EAT = "verb_eat"


# From
EVENT_VERB_PICKUP = "verb_pickup"

EVENT_VERB_DROP = "verb_drop"


# From
EVENT_VERB_CHECK_INVENTORY = "verb_check_inventory"


# From
EVENT_VERB_OPEN_DOOR = "verb_open_door"


# From ComponentItem.attempt_pickup(), called on an object to add another object to the first one's inventory, should they have one (object_to_add<PhysObj>, silent<bool>)
# Return EVENT_RETVAL_BLOCK_INVENTORY_ADD to block the addition
EVENT_INVENTORY_ADD_OBJECT = "inventory_add_object"
EVENT_RETVAL_BLOCK_INVENTORY_ADD = "block_inventory_add"

# From ComponentItem.attempt_drop(), called on an object to drop an item from its inventory (object_to_remove<PhysObj>, silent<bool>)
# Return EVENT_RETVAL_BLOCK_INVENTORY_REMOVE to block the removal
EVENT_INVENTORY_REMOVE_OBJECT = "inventory_remove_object"
EVENT_RETVAL_BLOCK_INVENTORY_REMOVE = "block_inventory_remove"

# From Player.find_nearby_objects_by_name(), called on an object to return a list of its inventory objects, should it have the component ()
EVENT_INVENTORY_GET_CONTENTS = "inventory_get_contents"

# From ComponentInventory.on_attempt_object_add(), called on an object when it is being added to an inventory. (inventory_owner<PhysObj>, inventory<ComponentInventory>)
# Return EVENT_RETVAL_BLOCK_INVENTORY_ADD to block the addition
EVENT_OBJECT_ADDING_TO_INVENTORY = "object_adding_to_inventory"
EVENT_RETVAL_BLOCK_OBJECT_INVENTORY_ADD = "block_object_inventory_add"

# From ComponentInventory.on_attempt_object_remove(), called on an object when it is being removed from an inventory. (inventory_owner<PhysObj>, inventory<ComponentInventory>)
# Return EVENT_RETVAL_BLOCK_INVENTORY_ADD to block the addition
EVENT_OBJECT_REMOVING_FROM_INVENTORY = "object_removing_from_inventory"
EVENT_RETVAL_BLOCK_OBJECT_INVENTORY_REMOVE = "block_object_inventory_remove"


# From ComponentInventory.object_add(), called on an object when it has been added to an inventory. (inventory_owner<PhysObj>, inventory<ComponentInventory>)
EVENT_OBJECT_ADDED_TO_INVENTORY = "object_added_to_inventory"

# From ComponentInventory.object_remove(), called on an object when it has been added to an inventory. (inventory_owner<PhysObj>, inventory<ComponentInventory>)
EVENT_OBJECT_REMOVED_FROM_INVENTORY = "object_removed_from_inventory"


# From Player.look_around_room(), called on everything in a room when the player looks around, which counts the first entry, too ()
# Return EVENT_RETVAL_BLOCK_BASEOBJ_PRINT_DESCRIPTION to prevent that baseobj's desc from being printed
# Return EVENT_RETVAL_BLOCK_ALL_PRINT_DESCRIPTION (ONLY FROM THE ROOM, NOT OBJECTS) to prevent everything in the room from being printed, does block all the normally-ensuing EVENT_BASEOBJ_PRINT_DESCRIPTION events as well
EVENT_BASEOBJ_PRINT_DESCRIPTION = "baseobj_print_description"
EVENT_RETVAL_BLOCK_BASEOBJ_PRINT_DESCRIPTION = "block_baseobj_print_description"
EVENT_RETVAL_BLOCK_ALL_PRINT_DESCRIPTION = "block_all_print_description"