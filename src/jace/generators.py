from time import sleep

from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from src.jace.database import generate_catalog_table
from src.scryfall.config import catalog_endpoints


def generate_table() -> Table:
    """Make a new table."""
    table = Table()
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Count")

    return table


job_progress = Progress(
    "[progress.description]{task.description}",
    SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    TextColumn("{task.fields[current]}"),
    TimeElapsedColumn(),
)

# job1 = job_progress.add_task("[green]Download Rules")
catalog_job = job_progress.add_task("[magenta]Generate Catalogs", total=len(catalog_endpoints), name='c', current=None)
# job3 = job_progress.add_task("[cyan]Generate Card Rulings", total=400)

total = sum(task.total for task in job_progress.tasks)
overall_progress = Progress()
overall_task = overall_progress.add_task("All Jobs", total=int(total))

progress_table = Table.grid()
progress_table.add_row(
    Panel.fit(
        overall_progress, title="Overall Progress", border_style="green", padding=(2, 2)
    ),
    Panel.fit(job_progress, title="[b]Jobs", border_style="red", padding=(1, 2)),
)

with Live(progress_table, refresh_per_second=10) as live:
    while not overall_progress.finished:
        sleep(0.1)
        for job in job_progress.tasks:
            if job.fields.get('name') == 'c':
                len_of_task = len(catalog_endpoints)
                tbl = generate_table(catalog_endpoints)
                for idx, n in enumerate(catalog_endpoints):
                    job.fields['current'] = n
                    tbl.add_row(
                        f"{idx}", n, f"[green]{generate_catalog_table(table=n)}"
                    )
                    job_progress.update(tbl)

                    if not job.finished:
                        job_progress.advance(job.id)

        completed = sum(task.completed for task in job_progress.tasks)
        overall_progress.update(overall_task, completed=completed)