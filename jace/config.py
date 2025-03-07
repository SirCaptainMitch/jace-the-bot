import os.path
from rich.console import Console
import signal
from threading import Event


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


if __name__ == '__main__':
    pass

