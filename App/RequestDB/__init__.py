def turnOffApostrophe(text)->str:
    """
    Turn off apostrophe in text with \'
    :param text: text to turn off apostrophe
    :return: text with apostrophe turned off
    """
    return text.replace("'", "\\'")
