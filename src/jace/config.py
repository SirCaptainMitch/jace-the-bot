import os
import os.path
import logging
from rich.console import Console
from rich.logging import RichHandler
import signal
from threading import Event

# rich.progress


from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

progress = Progress(
    TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
    BarColumn(bar_width=40),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    # DownloadColumn(),
    "•",
    # TransferSpeedColumn(),
    "•",
    TimeRemainingColumn(),
)


done_event = Event()


def handle_sigint(signum, frame):
    done_event.set()


signal.signal(signal.SIGINT, handle_sigint)

console: Console = Console()
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_PATH = os.path.join(ROOT_DIR, './.cache')

# FORMAT = "%(message)s"
# logging.basicConfig(
#     level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
# )
# log = logging.getLogger("rich")


if __name__ == '__main__':
    pass

