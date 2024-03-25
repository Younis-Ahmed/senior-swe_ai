"""
This module is responsible for creating panels for the chatbox and other components. 
It uses the rich library to create panels.
"""
from rich.panel import Panel
from rich.console import Console
from rich.columns import Columns


class PanelBase:
    """This class is responsible for creating panels for the chatbox and other components."""

    def __init__(self, title, width=50):
        self.title: str = title
        self.width: int = width
        self.console = Console()
        self._queue = Queue()

    def _create_base_panel(self) -> Panel:
        """Create a base panel for the chatbox."""
        chatboxes = self._queue.queue
        return Panel(
            Columns(chatboxes), title=self.title, expand=True,
            border_style="cyan", padding=(1, 1), title_align="center"
        )

    def _cache_content(self, content: Panel):
        """Cache the content of the chatbox."""
        self._queue.enqueue(content)

    def create_chatbox(self, title, content, width=50, is_ai=True):
        """Create a chatbox panel."""
        if not is_ai:
            chatbox = Panel.fit(content, width=width,
                                title=title, border_style="blue")
        else:
            chatbox = Panel.fit(content, width=width,
                                title=title, border_style="green")
        self._cache_content(chatbox)
        return chatbox

    def print_stdout(self):
        """Print the panel."""
        if self._queue.size() > 0:
            self.console.print(self._create_base_panel())


class Queue:
    """A simple Queue class."""

    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        """Add an item to the end of the queue."""
        self.queue.append(item)

    def dequeue(self):
        """Remove an item from the front of the queue."""
        if not self.is_empty():
            return self.queue.pop(0)
        return None

    def is_empty(self):
        """Check if the queue is empty."""
        return len(self.queue) == 0

    def size(self):
        """Get the size of the queue."""
        return len(self.queue)


if __name__ == "__main__":
    panel = PanelBase("Chat Panel", width=70)
    while True:
        user = input("User: ")
        panel.create_chatbox("User", user, is_ai=False)
        panel.print_stdout()
        ai = input("AI: ")
        panel.create_chatbox("AI", ai)
        panel.print_stdout()
    
