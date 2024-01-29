from typing import TYPE_CHECKING
from physical_obj import PhysObj
import events.events as events
import re
from packages.components.inventory import ComponentInventory
from packages.verbs._verb_names import VERB_LOOK_AROUND
from packages.elements._element_names import ELEMENT_INVISIBLE
from events.events import EVENT_INVENTORY_GET_CONTENTS, \
                        EVENT_BASEOBJ_PRINT_DESCRIPTION, \
                        EVENT_RETVAL_BLOCK_BASEOBJ_PRINT_DESCRIPTION, \
                        EVENT_RETVAL_BLOCK_ALL_PRINT_DESCRIPTION, \
                        EVENT_PLAYER_FIND_CONTENTS

if TYPE_CHECKING:
    import room
    from packages.verbs._verb import Verb
    from object import Object

class Player(PhysObj):
    
    def __init__(self) -> None:
        super().__init__()

        self.max_health: int = 100
        self.health = self.max_health

        # Bitflags for various player things
        self.player_flags = 0

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
            if (self.send_event(obj, EVENT_BASEOBJ_PRINT_DESCRIPTION) & EVENT_RETVAL_BLOCK_BASEOBJ_PRINT_DESCRIPTION):
                continue
                
            print(obj.desc)
    

    async def begin_taking_input(self):
        while(True):
            self.take_input()

    
    def take_input(self):
        user_input = input("\nWhat do you do?\n")
        self.parse_text(user_input)

    
    # The logic works as follows:
    # We have a word list, "a b c d e", when looking for verb "a b" with 2 arguments
    # We start with checking if "a b c d e" is a valid verb for self, objects, etc.
    # If not, then we move to "a b c d", and repeat, if the verb isn't found, then the function returns
    # Once we find "a b", then we move onto the args.
    # We check if "c d e" is a valid arg1, if not we go to "c d", etc.
    # Once we find that "c" is a valid arg1, then we go to arg2, and see that "d e" is a valid arg2, making the final verb "ab [c] [d e]"
    def parse_text(self, text_to_parse: str) -> bool:
        text_to_parse = re.sub(r" a\b| of\b| and\b| or\b| the\b| on\b| in\b| at\b| with\b", "", text_to_parse, flags=re.IGNORECASE).lower()
        word_list = text_to_parse.split(" ")

        command_tuples: list[tuple[(PhysObj | list[PhysObj]), int, "Verb"]] = self.check_command(word_list)
        if not command_tuples:
            return False
        
        working_tuples: list[tuple[tuple[(PhysObj | list[PhysObj]), int, "Verb"], list[PhysObj]]] = []

        for command_tuple in command_tuples:
            selected_object, words_used, verb = command_tuple
            arg_list = word_list.copy()
            words_used_list = list(range(words_used + 1)) # Doesn't count "read" in "read thing" due to start-at-0 memes
            words_used_list.reverse()
            for i in words_used_list: # 2, 1, 0
                arg_list.pop(i)
            
            if not len(arg_list):
                if not verb.can_execute_verb(selected_object):
                    continue

                working_tuples.append((command_tuple, []))
                continue
            
            final_arg_list = []
            
            for i in range(len(verb.expected_args)):
                return_tuple = self.arg_check(verb, arg_list, i)
                if not return_tuple:
                    continue

                argument, arg_words_used = return_tuple

                final_arg_list.append(argument) # Todo here: add a way  # What did he mean by this

                arg_words_used = list(range(arg_words_used))
                arg_words_used.reverse()
                break_outer = False
                for i in arg_words_used: # 2, 1, 0
                    arg_list.pop(i)
                    if not len(arg_list):
                        if not verb.can_execute_verb(selected_object, final_arg_list):
                            continue
                        
                        working_tuples.append((command_tuple, final_arg_list))
                        break_outer = True
                        break

                if break_outer:
                    break
            
            if not verb.can_execute_verb(selected_object, final_arg_list):
                continue

            working_tuples.append((command_tuple, final_arg_list))

        if len(working_tuples) == 0:
            return
        
        elif len(working_tuples) == 1:
            chosen_tuple, arglist = working_tuples[0]
            selected_object, words_used, verb = chosen_tuple
            verb.try_execute_verb(selected_object, arglist)
            return

        else:
            selection_string = "Which one? (by number)\n"
            tuple_number_dict: dict[int, tuple[(PhysObj | list[PhysObj], int, "Verb")]] = {}
            tuple_number = 1
            for tupl in working_tuples:
                chosen_tuple, arglist = tupl
                selected_object, words_used, verb = chosen_tuple
                tuple_number_dict[tuple_number] = tupl
                selection_string += f"({tuple_number}) {selected_object.name}\n"
                tuple_number += 1

            while True:
                picked_number = input(selection_string)

                if not picked_number.isnumeric():
                    continue

                picked_number = int(picked_number)

                try:
                    list(tuple_number_dict.keys()).index(picked_number)
                
                except ValueError:
                    continue

                chosen_tuple, arglist = tuple_number_dict[picked_number]
                selected_object, words_used, verb = chosen_tuple
                verb.try_execute_verb(selected_object, arglist)
                break

    def arg_check(self, verb: "Verb", arg_list: list[str], verb_argument_pos: int) -> tuple[(PhysObj | list[PhysObj]), int]:
        arg_list_len = len(arg_list)

        reverse_list = list(range(arg_list_len))
        reverse_list.reverse()

        for i in reverse_list:  
            argument = ""      
            for i2 in range(i + 1):
                if argument:
                    argument += f" {arg_list[i2]}"
                else:
                    argument += arg_list[i2]

                if isinstance(verb.expected_args[verb_argument_pos], str):
                    return (argument, i2)
                
                if isinstance(verb.expected_args[verb_argument_pos], int) and argument.isnumeric():
                    return (int(argument), i2)
                
                nearby_objects: list[PhysObj] = self.find_nearby_objects_by_name(argument)

                valid_objects: list[PhysObj] = []
                for nearby_obj in nearby_objects:
                    if isinstance(nearby_obj, verb.expected_args[verb_argument_pos]) and verb.argument_is_valid(nearby_obj, i2):
                        valid_objects.append(nearby_obj)
                
                if len(valid_objects) == 0:
                    continue
                
                elif len(valid_objects) == 1:
                    return (valid_objects[0], i2)
                
                else:
                    return (valid_objects, i2)
                
    
    def check_command(self, word_list: list[str]) -> list[tuple[(PhysObj | list[PhysObj]), int, "Verb"]]:
        valid_objects: list[tuple[PhysObj, int, "Verb"]] = []
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
                    item: PhysObj
                    verb = item.action_is_valid(command)
                    if verb:
                        valid_objects.append((item, i2, verb))
            
            for object in self.current_room.contents:
                if object == self:
                    continue
                
                verb = object.action_is_valid(command)
                if verb:
                    valid_objects.append((object, i2, verb))
                
                object_contents: list["Object"] = self.send_event(object, EVENT_PLAYER_FIND_CONTENTS) or []
                for contained_object in object_contents:
                    verb = contained_object.action_is_valid(command)
                    if verb:
                        valid_objects.append((contained_object, i2, verb))
                
        return valid_objects

    
    def find_nearby_objects_by_name(self, obj_name: str) -> list[PhysObj]: #feels odd having this on player, may change if i find smth better? #Maybe make it on baseobj and override?
        return_list: list[PhysObj] = []
        inventory_list = self.send_event(self, EVENT_INVENTORY_GET_CONTENTS)
        if inventory_list:
            for item in inventory_list:
                item: PhysObj
                if obj_name in item.alternate_names:
                    return_list.append(item)
                extra_items: list[PhysObj] = self.send_event(item, EVENT_PLAYER_FIND_CONTENTS) or []
                for extra_item in extra_items:
                    if obj_name in extra_item.alternate_names:
                        return_list.append(extra_item)

        for object in self.current_room.contents:
            if obj_name in object.alternate_names:
                return_list.append(object)
            extra_objects: list[PhysObj] = self.send_event(object, EVENT_PLAYER_FIND_CONTENTS) or []
            for extra_object in extra_objects:
                if obj_name in extra_object.alternate_names:
                    return_list.append(extra_object)
        
        return return_list