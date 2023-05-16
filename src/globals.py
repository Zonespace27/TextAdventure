from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base_obj import BaseObj

def initialize_globals():
    # Dict of "roomid" : Room reference
    global roomid_to_room

    roomid_to_room = {}

    # Dict of "objectid" : (dict of "data" : data)
    global object_id_data

    object_id_data = {}

    # Dict of "phys_objid" : (dict of "data" : data)
    global phys_obj_id_data

    phys_obj_id_data = {}

    # Dict of "verb_id" : Verb object
    global verb_id_data

    verb_id_data = {}

    # Ref to the player
    global player_ref

    player_ref = None
    
    # Dict of "component_id" : Component class
    global component_id_to_class

    component_id_to_class = {}


def get_subclasses_recursive(class_to_use: type) -> list[type]:
    return_list: list[type] = []
    for subclass in class_to_use.__subclasses__():
        return_list.append(subclass)
        return_list.extend(get_subclasses_recursive(subclass))
    
    return return_list


def qdel(object_to_delete: "BaseObj"):
    """
    Use this over the `del` function to delete objects
    """
    object_to_delete.dispose()
    del object_to_delete
