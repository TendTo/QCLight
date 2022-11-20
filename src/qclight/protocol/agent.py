"""Agent class."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .protocol import ProtocolEvents, ProtocolCallback, EventName
    from .message import Message


class Agent:
    """Agent that has an active role in the protocol."""

    def __init__(self, name: "str") -> "None":
        self.name = name
        self._events: "ProtocolEvents" = {
            "start": [],
            "message_sent": [],
            "message_received": [],
            "message_transmitted": [],
            "stop": [],
        }

    @property
    def events(self) -> "ProtocolEvents":
        """Events the agent will react to."""
        return self._events

    def get_events(self, event_name: "EventName") -> "list[ProtocolCallback]":
        """Gets the events the agent will react to."""
        return self._events[event_name]

    def set_events(
        self, event_name: "EventName", callbacks: "ProtocolCallback | list[ProtocolCallback]"
    ) -> "None":
        """Sets the events the agent will react to."""
        if not isinstance(callbacks, list):
            callbacks = [callbacks]
        self._events[event_name] = callbacks

    def add_event(self, event_name: "EventName", callback: "ProtocolCallback") -> "None":
        """Adds an event to the agent."""
        self._events[event_name].append(callback)

    def __repr__(self) -> "str":
        return f"Agent[{self.name}]"
