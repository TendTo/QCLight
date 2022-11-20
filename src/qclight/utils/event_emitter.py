"""EventEmitter class."""
from typing import Callable


class EventEmitter:
    """Event emitter used as a base class for other event emitting classes.
    It implements the event emitter pattern with the following methods:
    - :meth:`on` to add a callback to an event
    - :meth:`off` to remove a callback from an event
    - :meth:`emit` to emit an event
    """

    def __init__(self):
        self._events: "dict[str, list[Callable]]" = {}

    def on(self, event_name: str, callback: Callable) -> "None":
        """Adds a callback to an event.

        Args:
            event_name: name of the event
            callback: callback to add
        """
        self._events[event_name].append(callback)

    def emit(self, event_name: str, *args, **kwargs) -> "None":
        """Emits an event.

        Args:
            event_name: name of the event
            *args: arguments to pass to the callbacks
            **kwargs: keyword arguments to pass to the callbacks
        """
        for callbacks in self._events[event_name]:
            for callback in callbacks:  # type: ignore
                callback(*args, **kwargs)

    def off(self, event_name, callback) -> "None":
        """Removes a callback from an event.

        Args:
            event_name: name of the event
            callback: callback to remove
        """
        self._events[event_name].remove(callback)
