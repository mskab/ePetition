def remove_fields_from_dict(dictionary, fields):
    for field in fields:
        del dictionary[field]
    return dictionary