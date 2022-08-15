def remove_fields_from_dict(dictionary, fields):
    for field in fields:
        del dictionary[field]
    return dictionary


def list_of_dict_to_set_of_fsets(list_of_dict):
    """
    fsets - frozenset(s)
    """
    return set(frozenset(d.items()) for d in list_of_dict)
