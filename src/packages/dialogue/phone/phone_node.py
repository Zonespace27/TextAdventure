from .._node import DialogueNode


class PhoneNode(DialogueNode):
    def trigger_node(self) -> bool:
        super().trigger_node()
        return False

    def on_node_end(self):
        print("You put down the phone reciever, ending the call.")
