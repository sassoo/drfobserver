"""
    drfobserver.mixins
    ~~~~~~~~~~~~~~~~~~

    DRF object mixin to support an extremely simplistic observer
    pattern.
"""


__all__ = ('ObserverMixin',)


class ObserverMixin(object):
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

        super(ObserverMixin, self).__init__(*args, **kwargs)

        self._observers = {}
        for key, val in self.__class__.__dict__.items():
            if hasattr(val, '_observer_fields'):
                func = getattr(self, key)
                for field in func._observer_fields:
                    try:
                        self._observers[field].append(func)
                    except KeyError:
                        self._observers[field] = [func]
                # new object test
                if self.pk is None:
                    func()

    def __setattr__(self, name, value):
        """ Run the decorated method if its dependent field is changed

        NOTE: __setattr__ will be used by python before the constructor
              has even started to run! `_observers` won't be available
              until the constructor has finished.
        """

        super(ObserverMixin, self).__setattr__(name, value)

        try:
            for func in self._observers[name]:
                func()
        except (AttributeError, KeyError):
            pass
