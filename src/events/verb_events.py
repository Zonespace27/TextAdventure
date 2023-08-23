# From Verb.can_execute_verb(), called on the owning object to confirm that it will allow the verb to succeed (executing_verb<Verb>)
EVENT_VERB_CAN_EXECUTE = "verb_can_execute"
EVENT_RETVAL_BLOCK_VERB_EXECUTE = (1<<0)

# From VerbEat.execute_verb(), called on an object when the eat verb succeeds on it (eaten<bool>)
EVENT_VERB_EAT = "verb_eat"


# From
EVENT_VERB_PICKUP = "verb_pickup"

EVENT_VERB_DROP = "verb_drop"


# From
EVENT_VERB_CHECK_INVENTORY = "verb_check_inventory"


# From
EVENT_VERB_OPEN_DOOR = "verb_open_door"

EVENT_VERB_GET_UP = "verb_get_up"

EVENT_VERB_OPEN_CONTAINER = "verb_open_container"
EVENT_VERB_CLOSE_CONTAINER = "verb_close_container"

EVENT_VERB_EXAMINE = "verb_examine"