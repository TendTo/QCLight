"""Protocol class."""
from typing import Callable, TypedDict, Literal, overload, Any
from qclight.utils import EventEmitter
from .agent import Agent

MessageEventName = Literal["message_sent", "message_transmitted", "message_received"]
SetupEventName = Literal["start", "stop"]
EventName = Literal[SetupEventName, MessageEventName]
ProtocolCallback = Callable[["Protocol", EventName], None]
ProtocolMessageCallback = Callable[["Protocol", EventName, Any], None]


class ProtocolEvents(TypedDict):
    """Protocol events."""

    start: "list[ProtocolCallback]"
    message_sent: "list[ProtocolMessageCallback]"
    message_received: "list[ProtocolMessageCallback]"
    message_transmitted: "list[ProtocolCallback]"
    stop: "list[ProtocolCallback]"


class Protocol(EventEmitter):
    def __init__(self) -> None:
        super().__init__()
        self._agents: "set[Agent]" = set()
        self._events: ProtocolEvents = {
            "start": [],
            "message_sent": [],
            "message_transmitted": [],
            "message_received": [],
            "stop": [],
        }

    @overload
    def on(self, event_name: "SetupEventName", callback: "ProtocolCallback") -> "None":
        ...

    @overload
    def on(self, event_name: "MessageEventName", callback: "ProtocolMessageCallback") -> "None":
        ...

    def on(self, event_name: "EventName", callback: "Callable") -> "None":
        super().on(event_name, callback)

    @overload
    def emit(self, event_name: "SetupEventName") -> None:
        ...

    @overload
    def emit(self, event_name: "MessageEventName", message: Any) -> None:
        ...

    def emit(self, event_name: "EventName", message: Any = None) -> None:
        if message is None:
            super().emit(self, event_name)
        else:
            super().emit(self, event_name, message)

    def add_agent(self, *agents: "Agent") -> None:
        """Adds a participant to the protocol."""
        self._agents.union(agents)

    def receive_message(self, message: Any) -> None:
        """Receives a message from the protocol."""
        self.emit("message_received", message)

    def start(self) -> None:
        """Starts the protocol."""
        for agent in self._agents:
            for event_name, callback in agent.events.items():
                self.on(event_name, callback)  # type: ignore
        self.emit("start")

    def stop(self) -> None:
        """Ends the protocol."""
        self.emit("stop")
        for agent in self._agents:
            for event_name, callback in agent.events.items():
                self.off(event_name, callback)
