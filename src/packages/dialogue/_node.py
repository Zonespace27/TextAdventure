import global_textadv


class DialogueNode():

    def __init__(self, id: str, text: str, select_text: str, result_nodes: list[str], leave_allowed: bool, one_use_node: bool):
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

        # If True, the node is one-use and will revert to the previous node once used
        self.one_use_node: bool = one_use_node

        self.node_used: bool = False

    def trigger_node(self):
        print(self.text)
        if not self.one_use_node:
            self.offer_options()
        if self.one_use_node:
            return False
        return True

    def offer_options(self):
        options = self.result_nodes.copy()

        text_string: str = self.generate_option_text()

        while True:
            picked_number = input(text_string)

            if not picked_number.isnumeric():
                continue

            picked_number = int(picked_number)

            if len(options) - 1 < picked_number:
                continue

            if ("leave" in options) and (picked_number == options.index("leave")):
                self.on_node_end()
                return

            if global_textadv.dialogue_id_to_node[options[picked_number]].trigger_node():
                self.on_node_end()

            if global_textadv.dialogue_id_to_node[options[picked_number]].one_use_node:
                self.result_nodes.remove(options[picked_number])
                text_string = self.generate_option_text()
                options = self.result_nodes.copy()
                continue

            break

    def generate_option_text(self) -> str:
        options = self.result_nodes.copy()
        text_string: str = ""
        for node in options:
            text_string += f"({options.index(node)}) {global_textadv.dialogue_id_to_node[node].select_text}\n"

        if self.leave_allowed:
            options.append("leave")
            text_string += f"({options.index('leave')}) Leave\n"

        return text_string

    def on_node_end(self):
        return
