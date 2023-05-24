from typing import TYPE_CHECKING
import physical_obj
import events
import re
from packages.components.inventory import ComponentInventory
from packages.verbs._verb_names import VERB_LOOK_AROUND
from packages.elements._element_names import ELEMENT_INVISIBLE
from events import EVENT_INVENTORY_GET_CONTENTS, EVENT_BASEOBJ_PRINT_DESCRIPTION, EVENT_RETVAL_BLOCK_BASEOBJ_PRINT_DESCRIPTION, EVENT_RETVAL_BLOCK_ALL_PRINT_DESCRIPTION

if TYPE_CHECKING:
    import room
    from packages.verbs._verb import Verb

class Player(physical_obj.PhysObj):
    
    def __init__(self) -> None:
        super().__init__()

        self.max_health: int = 100
        self.health = self.max_health

        self.register_event(self, events.EVENT_PHYSOBJ_ENTERED_ROOM, self.on_enter_room)
        self.add_component(ComponentInventory, {"inventory_size": 5})
        self.add_element(ELEMENT_INVISIBLE)
        self.add_verb(VERB_LOOK_AROUND)


    def on_enter_room(self, source, entered_room: "room.Room"):
        """
        ### EVENT FUNCT
        """
        self.look_around_room(entered_room, entering_room = True)
    

    def look_around_room(self, room_to_look: "room.Room" = None, entering_room: bool = False):
        if not room_to_look:
            room_to_look = self.current_room

        event_retval: str = self.send_event(room_to_look, EVENT_BASEOBJ_PRINT_DESCRIPTION)
        if event_retval == EVENT_RETVAL_BLOCK_ALL_PRINT_DESCRIPTION:
            return
        
        print("\n")

        if not (event_retval == EVENT_RETVAL_BLOCK_BASEOBJ_PRINT_DESCRIPTION):
            print(room_to_look.desc)

        for obj in room_to_look.contents:
            if (self.send_event(obj, EVENT_BASEOBJ_PRINT_DESCRIPTION) == EVENT_RETVAL_BLOCK_BASEOBJ_PRINT_DESCRIPTION):
                continue
                
            print(obj.desc)
    

    def begin_taking_input(self):
        while(True):
            self.take_input()

    
    def take_input(self):
        user_input = input("What do you do?\n")
        self.parse_text(user_input)

    
    # The logic works as follows:
    # We have a word list, "a b c d e", when looking for verb "a b" with 2 arguments
    # We start with checking if "a b c d e" is a valid verb for self, objects, etc.
    # If not, then we move to "a b c d", and repeat, if the verb isn't found, then the function returns
    # Once we find "a b", then we move onto the args.
    # We check if "c d e" is a valid arg1, if not we go to "c d", etc.
    # Once we find that "c" is a valid arg1, then we go to arg2, and see that "d e" is a valid arg2, making the final verb "ab [c] [d e]"
    def parse_text(self, text_to_parse: str) -> bool:
        text_to_parse = re.sub(r" a\b| of\b| and\b| or\b| the\b| on\b| in\b| at\b", "", text_to_parse, flags=re.IGNORECASE).lower()
        word_list = text_to_parse.split(" ")

        command_tuples: list[tuple[physical_obj.PhysObj, int, "Verb"]] = self.check_command(word_list)
        if not command_tuples:
            return False
        
        for command_tuple in command_tuples:
            selected_object, words_used, verb = command_tuple
            arg_list = word_list.copy()
            words_used_list = list(range(words_used + 1)) # Doesn't count "read" in "read thing" due to start-at-0 memes
            words_used_list.reverse()
            for i in words_used_list: # 2, 1, 0
                arg_list.pop(i)
            
            if not len(arg_list):
                if not verb.try_execute_verb(selected_object):
                    continue
                return True
            
            final_arg_list = []
            
            for i in range(len(verb.expected_args)):
                return_tuple = self.arg_check(verb, arg_list, i)
                if not return_tuple:
                    continue

                argument, arg_words_used = return_tuple

                final_arg_list.append(argument)

                arg_words_used = list(range(arg_words_used))
                arg_words_used.reverse()
                for i in arg_words_used: # 2, 1, 0
                    arg_list.pop(i)
                    if not len(arg_list):
                        if not verb.try_execute_verb(selected_object, final_arg_list):
                            continue
                        return True
            
            if not verb.try_execute_verb(selected_object, final_arg_list):
                continue
            return True


    def arg_check(self, verb: "Verb", arg_list: list[str], verb_argument_pos: int) -> tuple:
        arg_list_len = len(arg_list)

        reverse_list = list(range(arg_list_len))
        reverse_list.reverse()

        for i in reverse_list:  
            argument = ""      
            for i2 in range(i + 1):
                argument += arg_list[i2]

                if isinstance(verb.expected_args[verb_argument_pos], str):
                    return (argument, i2)
                
                if isinstance(verb.expected_args[verb_argument_pos], int) and argument.isnumeric():
                    return (int(argument), i2)
                
                nearby_objects: list[physical_obj.PhysObj] = self.find_nearby_objects_by_name(argument)

                for nearby_obj in nearby_objects:
                    if isinstance(nearby_obj, verb.expected_args[verb_argument_pos]) and verb.argument_is_valid(nearby_obj, i2):
                        return (nearby_obj, i2)
                
    
    def check_command(self, word_list: list[str]) -> list[tuple[physical_obj.PhysObj, int, "Verb"]]:
        valid_objects: list[tuple[physical_obj.PhysObj, int, "Verb"]] = []
        word_list_reversed = list(range(len(word_list)))
        word_list_reversed.reverse()
        for i in word_list_reversed:
            command = ""
            for i2 in range(i + 1):
                command += ((" " if i2 > 0 else "") + word_list[i2]) # Starts with "a b c d e", goes to "a b c d", etc.
            verb = self.action_is_valid(command)
            if verb: # Even though the player's in the room's contents too, their stuff has priority
                valid_objects.append((self, i2, verb))
            
            inventory_list = self.send_event(self, EVENT_INVENTORY_GET_CONTENTS)
            if inventory_list:
                for item in inventory_list:
                    item: physical_obj.PhysObj
                    verb = item.action_is_valid(command)
                    if verb:
                        valid_objects.append((item, i2, verb))
            
            for object in self.current_room.contents: # might want to find a fix for this hitting the player again, but no biggie atm
                verb = object.action_is_valid(command)
                if verb:
                    valid_objects.append((object, i2, verb))
        return valid_objects

    
    def find_nearby_objects_by_name(self, obj_name: str) -> list[physical_obj.PhysObj]: #feels odd having this on player, may change if i find smth better? #Maybe make it on baseobj and override?
        return_list: list[physical_obj.PhysObj] = []
        inventory_list = self.send_event(self, EVENT_INVENTORY_GET_CONTENTS)
        if inventory_list:
            for item in inventory_list:
                item: physical_obj.PhysObj
                if obj_name in item.alternate_names:
                    return_list.append(item)

        for object in self.current_room.contents:
            if obj_name in object.alternate_names:
                return_list.append(object)
        
        return return_list