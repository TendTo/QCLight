"""Agent class."""
from typing import overload, Callable
from .protocol import (
    ProtocolEvents,
    ProtocolCallback,
    ProtocolMessageCallback,
    EventName,
    SetupEventName,
    MessageEventName,
)


class Agent:
    """Agent that has an active role in the protocol."""

    def __init__(self, name: "str") -> "None":
        self.name = name
        self._events: ProtocolEvents = {
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

    @overload
    def add_event(self, event_name: "SetupEventName", callback: "ProtocolCallback") -> "None":
        ...

    @overload
    def add_event(
        self, event_name: "MessageEventName", callback: "ProtocolMessageCallback"
    ) -> "None":
        ...

    def add_event(self, event_name: "EventName", callback: "Callable") -> "None":
        """Adds an event to the agent."""
        self._events[event_name].append(callback)

    def __str__(self) -> "str":
        return f"Agent {self.name}"
