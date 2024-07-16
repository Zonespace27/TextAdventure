class NonExistentJsonObject(Exception):
    """
    An exception raised by the json loader trying to create an object whose ID does not exist.
    """


class NonExistentDialogueNode(Exception):
    """
    An exception raised when a dialogue node ID is selected in a conversation when that node is not found in dialogue_id_to_node.
    """


class NoLocalizationLanguage(Exception):
    """
    An exception raised if there isn't a localization language selected.
    """


class StringNotLocalized(Exception):
    """
    An exception raised if a string is fed into Localization.localize() without being a proper localization string, but only if ERROR_NONLOCALIZED is True.
    """
