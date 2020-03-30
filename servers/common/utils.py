import datetime


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


def disable_keyword_argument_on_none(fn):
    """
    Removes "None" keyword arguments from the equation when calling functions
    """
    def wrapped(*args, **kwargs):
        return fn(*args, **{k: v for k, v in kwargs.items() if v is not None})
    return wrapped


def time_now_standard():
    """
    Gets the time now, in the ISO8601 format used throughout the code
    """
    time_now = datetime.datetime.utcnow()
    iso8601_now = time_now.strftime("%Y-%m-%dT%H:%M:%S%z")
    return iso8601_now
