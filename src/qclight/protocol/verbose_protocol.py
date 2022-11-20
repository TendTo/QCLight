"""Protocol class."""
import logging
from typing import TYPE_CHECKING
from .protocol import Protocol

if TYPE_CHECKING:
    from .message import Message


class VerboseProtocol(Protocol):
    """Extend the current protocol implementation to log all events to the console."""

    def start(self) -> "None":
        logging.info("Starting protocol")
        super().start()

    def send_message(self, message: "Message") -> "None":
        logging.info("Sending message %s", message)
        super().send_message(message)

    def transmit_message(self) -> "None":
        logging.info("Transmitting message %s", self.message)
        super().transmit_message()

    def receive_message(self) -> "None":
        logging.info("Received message %s", self.message)
        super().receive_message()

    def stop(self) -> "None":
        logging.info("Stopping protocol")
        super().stop()
