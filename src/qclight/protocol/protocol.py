"""Protocol class."""
from typing import TYPE_CHECKING, Callable, TypedDict, Literal
from qclight.utils import EventEmitter

if TYPE_CHECKING:
    from .agent import Agent
    from .message import Message

EventName = Literal["start", "stop", "message_sent", "message_transmitted", "message_received"]
ProtocolCallback = Callable[["Protocol"], None]


class ProtocolEvents(TypedDict):
    """Protocol events."""

    start: "list[ProtocolCallback]"
    message_sent: "list[ProtocolCallback]"
    message_received: "list[ProtocolCallback]"
    message_transmitted: "list[ProtocolCallback]"
    stop: "list[ProtocolCallback]"


class Protocol(EventEmitter):
    """Agents take part in the protocol by sending messages to each other,
    causing the protocol object to emit events that the agents can listen to and react to.

    The message can be intercepted by a bad actor, which can then modify the message
    before it is received by the intended recipient.
    """

    def __init__(self) -> "None":
        super().__init__()
        self.message: "Message | None" = None
        self._running = False
        self._agents: "set[Agent]" = set()
        self._events: ProtocolEvents = {
            "start": [],
            "message_sent": [],
            "message_transmitted": [],
            "message_received": [],
            "stop": [],
        }

    def on(self, event_name: "EventName", callback: "Callable") -> "None":
        super().on(event_name, callback)

    def emit(self, event_name: "EventName", *args, **kwargs) -> "None":
        super().emit(event_name, self, *args, **kwargs)

    def add_agent(self, *agents: "Agent") -> "None":
        """Adds a participant to the protocol."""
        self._agents = self._agents.union(agents)

    def start(self) -> "None":
        """Starts the protocol."""
        if self._running:
            raise Exception("Protocol already started")
        self._running = True
        for agent in self._agents:
            for event_name, callback in agent.events.items():
                self.on(event_name, callback)  # type: ignore
        self.emit("start")

    def send_message(self, message: "Message") -> "None":
        """Sends a message to the protocol."""
        self.message = message
        self.emit("message_sent")
        self.transmit_message()

    def transmit_message(self) -> "None":
        """Transmits a message to the protocol."""
        self.emit("message_transmitted")
        self.receive_message()

    def receive_message(self) -> "None":
        """Receives a message from the protocol."""
        self.emit("message_received")

    def stop(self) -> "None":
        """Ends the protocol."""
        self.emit("stop")
        for agent in self._agents:
            for event_name, callback in agent.events.items():
                self.off(event_name, callback)
        self._running = False
