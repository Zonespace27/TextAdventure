from .._node import DialogueNode
from global_textadv import output


class PhoneNode(DialogueNode):
    def trigger_node(self) -> bool:
        super().trigger_node()
        return False

    def on_node_end(self):
        output("You put down the phone reciever, ending the call.")
