import object
from packages.components.edible import ComponentEdible
import globals
from json import load


class Item(object.Object):
    def __init__(self) -> None:
        self.current_room = None
        self.object_components = {}

    def foobar(self):
        print("hello")
        globals.qdel(self)
        return "hi"


def test():
    word_list = ["a", "b", "c", "d", "e"]
    word_list_len = len(word_list)
    word_list_2 = list(range(word_list_len))
    word_list_2.reverse()
    for i in word_list_2:
        command = ""
        for i2 in range(i + 1):
            command += word_list[i2]
        if command == "a":
            return (i, i2)


def test_2():
    print(str(ComponentEdible.id))
    print(str(ComponentEdible().id))


def test_3():
    globals.initialize_globals()
    print(Item().foobar())


def test_4():
    file = load(open('json/phys_objects.json'))
    bar = None
    for id in file:
        bar = file[id]["foo"]
        print(bar)


test_4()
