from typing import TYPE_CHECKING
from exception import NonExistentJsonObject
import globals

if TYPE_CHECKING:
    from packages.components._component import Component
    from packages.verbs._verb import Verb
    from packages.elements._element import Element

class BaseObj(object):
    """
    The basis of everything, to allow for events to work. If it's an object that will be *inside* a room, use PhysObj instead of this.
    """

    def __init__(self, object_id: str = "") -> None:
        # Equivalent to signal_procs
        self.event_callbacks = {}
        # Equivalent to comp_lookup
        self.object_lookup = {}
        # A dict of class : component reference
        self.object_components: dict[type["Component"], "Component"] = {}
        # What verbs have this physobj as a source, based off of string ID
        self.source_verbs: list["Verb"] = []
        # A dict of "trait" : ["sources"], traits should be used when you want to have generic things (e.g. the inability to use verbs) possibly come from multiple sources at once
        self.traits: dict[str, list[str]] = {}

        if object_id:
            try:
                self.source_verbs = globals.object_id_data[object_id]["verbs"].copy()
            except KeyError:
                raise NonExistentJsonObject

            for component_id in list(globals.object_id_data[object_id]["components"].keys()):
                component_id: str
                key_index: int = list(globals.object_id_data[object_id]["components"].keys()).index(component_id)
                dictkey: str = list(globals.object_id_data[object_id]["components"].keys())[key_index]
                self.add_component(globals.component_id_to_class[component_id], globals.object_id_data[object_id]["components"][dictkey]) # There's a better way to do this i'm sure
            
            for element_id in globals.object_id_data[object_id]["elements"]:
                self.add_element(element_id)

    
    def dispose(self):
        """
        Used for reference cleanup PRIOR to deletion being called.
        The reason this is used over __del__ is that del is the destructor for *after* the ref count has hit 0
        """
        for component in list(self.object_components.values()):
            globals.qdel(component)

        self.source_verbs = []


    def register_event(self, target: "BaseObj", event_type: str, func_to_callback, override = False): #Some time, make sure that an object with signals elsewhere being deleted doesn't cause fuckery
        try:
            target_callbacks = self.event_callbacks[target]

        except KeyError:
            target_callbacks = {}

        lookup = target.object_lookup
        if not lookup:
            lookup = {}

        if ((event_type in list(target_callbacks.keys())) and not override):
            print(f"{event_type} overriden, set override = True to suppress this warning.")
        
        target_callbacks[event_type] = func_to_callback
        self.event_callbacks[target] = target_callbacks
        # Equivalent to looked_up
        lookup_list: list = []
        try:
            lookup_list = lookup[event_type]

        except KeyError:
            lookup[event_type] = self

        if (lookup_list == self):
            return
        
        elif (not isinstance(lookup_list, list)):
            lookup[event_type] = [lookup_list, self]
            
        else:
            lookup_list.append(self)
        
        target.object_lookup = lookup
    

    def unregister_event(self, target: "BaseObj", event_or_events):
        lookup: dict = target.object_lookup
        if not (self.event_callbacks or self.event_callbacks[target] or lookup):
            return

        if not isinstance(event_or_events, list):
            event_or_events = [event_or_events]

        for event in event_or_events:
            if not self.event_callbacks[target][event]:
                continue

            if isinstance(lookup[event], list):
                lookup_event_len = len(lookup[event])

                if lookup_event_len == 2:
                    lookup[event] = (lookup[event] - self)[0]
                
                elif lookup_event_len == 1:
                    if not (self in lookup[event]):
                        continue
                    
                    lookup.pop(event)
                    if not len(lookup):
                        target.object_lookup = None
                        break
                
                elif lookup_event_len == 0:
                    if not (lookup[event] == self):
                        continue
                    
                    lookup.pop(event)
                    if not len(lookup):
                        target.object_lookup = None
                        break
                
                else:
                    lookup[event].remove(self)
            
            else:
                lookup.pop(event)

        for event in event_or_events:
            self.event_callbacks[target].pop(event)
        if not len(self.event_callbacks[target]):
            self.event_callbacks.pop(target)


    def _send_event(self, event: str, *args):
        target = self.object_lookup[event]
        
        if not isinstance(target, list): 
            listening_object = target #Type me later
            try:
               method_to_call = listening_object.event_callbacks[self][event]

            except AttributeError:
                print(f"{listening_object.event_callbacks[self][event]} isn't an attribute of {listening_object}.") # Check if this runtimes either lmao
            
            except KeyError: # The object no longer exists in the listening_object's event_callbacks
                return
            
            arglist = []
            for i in range(len(args[0])):
                arglist.append(args[0][i])
            
            return method_to_call(*arglist)

        # Basically, this exists to allow for objects to unregister in the event itself, but still let every other listening object recieve the event too
        queued_calls: dict = {}

        for listening_object in target: #fixme
            queued_calls[listening_object] = listening_object.event_callbacks[self][event]
        
        return_bitflag: int = 0
        for listening_object in queued_calls:
            try:
                method_to_call = listening_object.event_callbacks[self][event] 

            except AttributeError:
                print(f"{listening_object.event_callbacks[self][event]} isn't an attribute of {listening_object}.") # Check if this runtimes either lmao      
            
            return_bitflag |= (method_to_call(*args) or 0)
        
        return return_bitflag
    

    def send_event(self, target: "BaseObj", event: str, *args) -> int:
        """
        This method is used to send an event to a target. See `docs/signals.md` for detail on how signals work.\n
        This will only ever return BITFLAGS. Never check the return value of this with `==`, always use `&`.
        """
        if not (target.object_lookup):
            return 0
        
        if not (event in list(target.object_lookup.keys())):
            return 0
        
        return target._send_event(event, [target, *args]) or 0 # Since we're always returning a bitflag, return 0 if the event doesn't return anything


    def add_component(self, component_class: type["Component"], arg_dict: dict[str]):
        if isinstance(arg_dict, list): # For the inherent components that are a list by default
            arg_dict = arg_dict[0]

        component_class(arg_dict).attempt_attachment(self)


    def get_component(self, component_class: type["Component"]) -> "Component":
        if component_class not in list(self.object_components.keys()):
            return None

        return self.object_components[component_class]

    
    def remove_component(self, component_class: type["Component"]):
        globals.qdel(self.object_components[component_class]) # TODO: Make sure this cleans up the key


    def add_verb(self, verb_id: str) -> bool:
        if verb_id not in globals.verb_id_data:
            return False
        
        if globals.verb_id_data[verb_id] in self.source_verbs:
            return True

        verb: "Verb" = globals.verb_id_data[verb_id]
        
        if not verb.can_attach_to(self):
            return False

        self.source_verbs.append(globals.verb_id_data[verb_id])
        return True


    def remove_verb(self, verb_id: str) -> bool:
        if verb_id not in list(globals.verb_id_data.keys()):
            return False
    
        if not (globals.verb_id_data[verb_id] in self.source_verbs):
            return True
        
        self.source_verbs.remove(globals.verb_id_data[verb_id])
        return True
    

    def add_element(self, element_id: str) -> bool:
        if element_id not in list(globals.element_id_to_ref.keys()):
           return False

        element: "Element" = globals.element_id_to_ref[element_id]
        return element.hook_object(self)
    

    def remove_element(self, element_id: str) -> bool:
        if element_id not in list(globals.element_id_to_ref.keys()):
           return False

        element: "Element" = globals.element_id_to_ref[element_id]
        return element.unhook_object(self)


    def add_trait(self, trait_to_add: str, trait_source: str):
        if trait_to_add in self.traits:
            self.traits[trait_to_add].append(trait_source)
        
        else:
            self.traits[trait_to_add] = [trait_source]

    
    def remove_trait(self, trait_to_remove: str, trait_source: str):
        if not (trait_to_remove in self.traits):
            return
        
        if not (trait_source in self.traits[trait_to_remove]):
            return
        
        self.traits[trait_to_remove].remove(trait_source)
        if not len(self.traits[trait_to_remove]):
            self.traits.pop(trait_to_remove)
    

    def force_remove_trait(self, trait_to_remove: str):
        """
        Remove a trait no matter what or how many sources it has. Use with care.
        """
        if not (trait_to_remove in self.traits):
            return

        self.traits.pop(trait_to_remove)

    
    def has_trait(self, trait_to_find: str) -> bool:
        """
        Returns True if self has the specified trait from any source, returns False otherwise.
        """
        return (trait_to_find in self.traits)
    

    def has_trait_from(self, trait_to_find: str, trait_source: str) -> bool:
        """
        Returns True if self has the specified trait from specified source, returns False otherwise.
        """
        if not (trait_to_find in self.traits):
            return False
        
        return (trait_source in self.traits[trait_to_find])
