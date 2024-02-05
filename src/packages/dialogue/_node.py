import global_textadv


class DialogueNode():

    def __init__(self, id: str, text: str, select_text: str, result_nodes: list[str], leave_allowed: bool):
        # The unique ID of this dialogue node
        self.id: str = id

        # The content text of this node of dialogue
        self.text: str = text

        # The text shown when selecting a dialogue choice
        self.select_text: str = select_text

        # All dialogue nodes that will be presented to the player after this node is chosen
        self.result_nodes: list[str] = result_nodes

        # If the player is allowed to leave dialogue at the end of this node
        self.leave_allowed: bool = leave_allowed

    def trigger_node(self):
        print(self.text)
        self.offer_options()

    def offer_options(self):
        options = self.result_nodes.copy()
        if self.leave_allowed:
            options.append("leave")

        text_string: str = ""
        for node in options:
            text_string += f"({options.index(node)}) {global_textadv.dialogue_id_to_node[options[picked_number]].select_text}\n"

        while True:
            picked_number = input(text_string)

            if not picked_number.isnumeric():
                continue

            picked_number = int(picked_number)

            if len(options) - 1 < picked_number:
                continue

            global_textadv.dialogue_id_to_node[options[picked_number]].trigger_node(
            )
            break
