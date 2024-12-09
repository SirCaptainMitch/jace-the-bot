# %%
from time import sleep

from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.console import Console
from jace.database import (
    generate_catalog_table
    , generate_oracle_cache
    , generate_default_cards_cache
    , generate_card_rulings_cache
    , generate_unique_artwork_cache
    , generate_all_cards_cache
)
from scryfall.config import catalog_endpoints

console = Console()

# %%
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

job1 = job_progress.add_task("[green]Download Rules", total=1, name='download_comprehensive_rules', current=None)
catalog_job = job_progress.add_task("[magenta]Generate Catalogs", total=len(catalog_endpoints), name='generate_catalog_table', current=None)
catalog_job = job_progress.add_task("[magenta]Generate All Cards", total=1, name='generate_scryfall_all_cards', current=None)
catalog_job = job_progress.add_task("[magenta]Generate Unique Artwork", total=1, name='generate_scryfall_artwork', current=None)
catalog_job = job_progress.add_task("[magenta]Generate Default Cards", total=1, name='generate_scryfall_default_cards', current=None)
catalog_job = job_progress.add_task("[magenta]Generate Card Rulings", total=1, name='generate_scryfall_rulings', current=None)
catalog_job = job_progress.add_task("[magenta]Generate Oracle Cards", total=1, name='generate_scryfall_oracle', current=None)
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

# %%

with Live(progress_table, refresh_per_second=100) as live:
    while not overall_progress.finished:
        sleep(0.1)
        tbl = generate_table()
        for job in job_progress.tasks:

            match job.fields.get('name'):
                case 'download_comprehensive_rules':
                    job.fields['current'] = 'DL'
                    tbl.add_row(
                        f"{0}", 'download_rules', f"[green]1-2-3-4-5"
                    )
                    job_progress.update(job.id)
                    if not job.finished:
                        job_progress.advance(job.id)
                case 'generate_catalog_table':
                    len_of_task = len(catalog_endpoints)
                    for idx, n in enumerate(catalog_endpoints):
                        job.fields['current'] = n
                        tbl.add_row(
                            f"{idx}", n, f"[green]{generate_catalog_table(table=n)}"
                        )
                        try:
                            job_progress.update(job.id)
                        except BaseException as e:
                            console.print_exception()

                        if not job.finished:
                            job_progress.advance(job.id)
                case 'generate_scryfall_all_cards':
                    job.fields['current'] = 1
                    tbl.add_row(
                        f"{idx}", n, f"[green]{generate_all_cards_cache()}"
                    )
                    try:
                        job_progress.update(job.id)
                    except BaseException as e:
                        console.print_exception()

                    if not job.finished:
                        job_progress.advance(job.id)
                case 'generate_scryfall_artwork':
                    job.fields['current'] = 1
                    tbl.add_row(
                        f"{idx}", n, f"[green]{generate_unique_artwork_cache()}"
                    )
                    try:
                        job_progress.update(job.id)
                    except BaseException as e:
                        console.print_exception()

                    if not job.finished:
                        job_progress.advance(job.id)
                case 'generate_scryfall_default_cards':
                    job.fields['current'] = 1
                    tbl.add_row(
                        f"{idx}", n, f"[green]{generate_default_cards_cache()}"
                    )
                    try:
                        job_progress.update(job.id)
                    except BaseException as e:
                        console.print_exception()

                    if not job.finished:
                        job_progress.advance(job.id)
                case 'generate_scryfall_rulings':
                    job.fields['current'] = 1
                    tbl.add_row(
                        f"{idx}", n, f"[green]{generate_card_rulings_cache()}"
                    )
                    try:
                        job_progress.update(job.id)
                    except BaseException as e:
                        console.print_exception()

                    if not job.finished:
                        job_progress.advance(job.id)
                case 'generate_scryfall_oracle':
                    job.fields['current'] = 1
                    tbl.add_row(
                        f"{idx}", n, f"[green]{generate_oracle_cache()}"
                    )
                    try:
                        job_progress.update(job.id)
                    except BaseException as e:
                        console.print_exception()

                    if not job.finished:
                        job_progress.advance(job.id)

        completed = sum(task.completed for task in job_progress.tasks)
        overall_progress.update(overall_task, completed=completed)
