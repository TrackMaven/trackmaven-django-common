from django.shortcuts import _get_queryset


def get_object_or_make(klass, *args, **kwargs):
    """
    The long lost sibling of Django's `get_or_create`.

    Attempts to look for and get a model, if none is found, just populates
    the model class with the look up fields.

    Example:

        >>> instance, exists = get_object_or_make(Post, url="http://trackmaven.com")
        >>> instance.pk
        1
        >>> exists
        True


    Returns:

        object: The django model passed in
        exists (boolean): An boolean specifying whether an object was found.

    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs), True
    except queryset.model.DoesNotExist:
        return klass(*args, **kwargs), False
