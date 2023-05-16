from typing import TYPE_CHECKING
import physical_obj
import events
import re

if TYPE_CHECKING:
    import room
    import item
    from packages.verbs._verb import Verb

class Player(physical_obj.PhysObj):
    
    def __init__(self, object_id: str = "") -> None:
        super().__init__(object_id)

        self.max_health: int = 100
        self.health = self.max_health
        self.inventory: list["item.Item"] = []

        self.player_visible = False

        self.register_event(self, events.EVENT_PHYSOBJ_ENTERED_ROOM, self.on_enter_room)


    def on_enter_room(self, source, entered_room: "room.Room"):
        """
        ### EVENT FUNCT
        """
        print(entered_room.desc)

        for obj in entered_room.contents:
            if not obj.player_visible:
                continue
                
            print(obj.desc)


    def begin_taking_input(self):
        while(True):
            self.take_input()
            
    
    def take_input(self):
        user_input = input("")
        self.parse_text(user_input)

    
    # The logic works as follows:
    # We have a word list, "a b c d e", when looking for verb "a b" with 2 arguments
    # We start with checking if "a b c d e" is a valid verb for self, objects, etc.
    # If not, then we move to "a b c d", and repeat, if the verb isn't found, then the function returns
    # Once we find "a b", then we move onto the args.
    # We check if "c d e" is a valid arg1, if not we go to "c d", etc.
    # Once we find that "c" is a valid arg1, then we go to arg2, and see that "d e" is a valid arg2, making the final verb "ab [c] [d e]"
    def parse_text(self, text_to_parse: str) -> bool:
        text_to_parse = re.sub(r" a\b| of\b| and\b| or\b| the\b| on\b", "", text_to_parse, flags=re.IGNORECASE).lower()
        word_list = text_to_parse.split(" ")

        command_tuple: tuple[physical_obj.PhysObj, int, "Verb"] = self.check_command(word_list)
        if not command_tuple:
            return False
        
        selected_object, words_used, verb = command_tuple

        arg_list = word_list.copy()
        words_used_list = list(range(words_used + 1)) # Doesn't count "read" in "read thing" due to start-at-0 memes
        words_used_list.reverse()
        for i in words_used_list: # 2, 1, 0
            arg_list.pop(i)
        
        if not len(arg_list):
            verb.try_execute_verb(selected_object)
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
                    verb.try_execute_verb(selected_object, final_arg_list)
                    return True
        
        verb.try_execute_verb(selected_object, final_arg_list)
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
                
                nearby_obj = self.find_nearby_object_by_name(argument)

                if nearby_obj and isinstance(nearby_obj, verb.expected_args[verb_argument_pos]):
                    return (nearby_obj, i2)
                
    
    def check_command(self, word_list: list[str]) -> tuple[physical_obj.PhysObj, int, "Verb"]:
        word_list_reversed = list(range(len(word_list)))
        word_list_reversed.reverse()
        for i in word_list_reversed:
            command = ""
            for i2 in range(i + 1):
                command += ((" " if i2 > 0 else "") + word_list[i2]) # Starts with "a b c d e", goes to "a b c d", etc.
                verb = self.action_is_valid(command)
                if verb: # Even though the player's in the room's contents too, their stuff has priority
                    return (self, i2, verb)
                
                for item in self.inventory:
                    verb = item.action_is_valid(command)
                    if verb:
                        return (item, i2, verb)
                
                for object in self.current_room.contents: # might want to find a fix for this hitting the player again, but no biggie atm
                    verb = object.action_is_valid(command)
                    if verb:
                        return (object, i2, verb)
        return None

    
    def find_nearby_object_by_name(self, obj_name: str) -> physical_obj.PhysObj: #feels odd having this on player, may change if i find smth better? #Maybe make it on baseobj and override?
        for item in self.inventory:
            if obj_name in item.alternate_names:
                return item

        for object in self.current_room.contents:
            if obj_name in object.alternate_names:
                return object
        
        return None