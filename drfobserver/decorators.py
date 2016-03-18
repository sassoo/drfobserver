"""
    drfobserver.decorators
    ~~~~~~~~~~~~~~~~~~~~~~

    DRF object field decorators to support an extremely simplistic
    observer pattern.
"""


__all__ = ('observer',)


def observer(*fields):
    """ Observer decorator

    In addition to wrapping a function like any decorator the
    `observer` decorator takes `*args` which represent django
    field names that should be observed for mutations.

    The `ObserverMixin` is responsible for monitoring the fields
    for mutation & acting on it but the decorator takes the list
    of fields to observe & adds them to the wrapped function as
    a hidden property named `_observer_fields`.

    The decorator is really just syntactic sugar to declare the
    fields that should be monitored right above the method that
    should be run.
    """

    def observer_wrapper(func):
        """ Add the hidden property with the fields to observe """
        func._observer_fields = fields
        return func
    return observer_wrapper
