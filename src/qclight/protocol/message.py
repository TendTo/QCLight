"""Message class."""
from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from .agent import Agent


@dataclass
class Message:
    """Generic message sent by an agent to another."""

    sender: "Agent"
    receiver: "Agent"
    content: "str"

    def __str__(self) -> "str":
        return f"Message[from {self.sender} to {self.receiver}: {self.content}]"
