def remove_directories(list_of_keys):
    """
    Removes directories from a list of S3 keys.
    """
    return [path for path in filter(lambda x: x[-1] != '/', list_of_keys)]


def extract_key_with_identifier_from_ObjectSummary(identifier, objSumList):
    """
    Extracts the key from ObjectSummary list
    """
    return [objSum.key for objSum in filter(
        lambda x: x.key.find(identifier) == 0, objSumList
    )]
