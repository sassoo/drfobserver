"""
    drfobserver.mixins
    ~~~~~~~~~~~~~~~~~~

    DRF object mixin to support an extremely simplistic observer
    pattern.
"""

from collections import defaultdict


__all__ = ('ObserverMixin',)


class ObserverMixin:
    """ Simplistic observer pattern mixin

    This is to keep fields in sync when dependent fields are mutated.
    It will only work with methods that have the `observer` decorator
    & overrides `__setattr__` to determine if the mutation requires
    a side-effect.

    To avoid much computational overhead, all observed fields are
    collected in the constructor & stored in a hidden property on
    the object named `_observers`. The items in the dict are the
    wrapped methods themselves & will be called in a, probably,
    unpredictable order.
    """

    def __init__(self, *args, **kwargs):
        """ Create a dict of all observed setters

        Addtionally, invoke each method to ensure all fields have
        the latest data if the object is NEW.
        """

        super().__init__(*args, **kwargs)

        self._observers = defaultdict(list)
        props = filter(lambda p: p.startswith('_observe_'), dir(self))

        for prop in props:
            func = getattr(self, prop)
            for field in getattr(func, '_observed_fields', ()):
                self._observers[field].append(func)
                if self.pk is None:
                    func()

    def __setattr__(self, name, value):
        """ Run the decorated method if its dependent field is changed

        NOTE: __setattr__ will be used by python before the constructor
              has even started to run! `_observers` won't be available
              until the constructor has finished.
        """

        super().__setattr__(name, value)

        try:
            for func in self._observers[name]:
                func()
        except (AttributeError, KeyError):
            pass
