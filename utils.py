def convert_dict_keys_to_camelCase(dictionary):
    """
    Converts all keys of a Python dict from snake_case to camelCase

    Args:
        dict (dict): Python dictionary with keys in snake_case

    Returns:
        dict: input dictionary with keys in camelCase
    """

    ret = {}
    for val in dictionary:
        ret[snake_to_camelCase(val)] = dictionary.get(val)

    return ret

def snake_to_camelCase(string):
    """
    Converts a snake_case string into a camelCase string

    Args:
        string (str): string in snake_case
    """
    tokens = string.split('_')
    out = tokens[0]
    for tok in tokens[1:]:
        out += tok.capitalize()

    return out
