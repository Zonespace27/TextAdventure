import object
from packages.components.edible import ComponentEdible

class Item(object.Object):
    pass




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

test_2()