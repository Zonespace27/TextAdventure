class NonExistentJsonObject(Exception):
    """
    An exception raised by the json loader trying to create an object whose ID does not exist.
    """


class NonExistentDialogueNode(Exception):
    """
    An exception raised when a dialogue node ID is selected in a conversation when that node is not found in dialogue_id_to_node.
    """
