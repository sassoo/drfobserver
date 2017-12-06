"""
    drfobserver.decorators
    ~~~~~~~~~~~~~~~~~~~~~~

    DRF object field decorators to support an extremely simplistic
    observer pattern.
"""


__all__ = ('observer',)


def observer(*fields):
    """ Observer decorator

    The `observer` decorator takes `*args` which represent django
    field names that should be observed for mutations.

    The `ObserverMixin` is responsible for monitoring the fields
    for mutation & acting on it but the decorator takes the list
    of fields to observe & adds them to the wrapped function as
    a private `_observed_fields` property.
    """

    def observer_wrapper(func):
        """ Add the hidden property with the fields to observe """

        assert func.__name__.startswith('_observe_'), \
            'Observed method names must begin with "_observer_" not %s' % func.__name__
        # pylint: disable=protected-access
        func._observed_fields = fields
        return func
    return observer_wrapper
