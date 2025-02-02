#!/usr/bin/env python3
"""
Refactored progress tracker using Rich Live.
"""

from time import sleep
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from jace.database import (
    generate_catalog_table,
    generate_oracle_cache,
    generate_default_cards_cache,
    generate_card_rulings_cache,
    generate_unique_artwork_cache,
    generate_all_cards_cache,
)
from scryfall.config import catalog_endpoints

console = Console()


def create_table() -> Table:
    """Create a new table with standard columns."""
    table = Table()
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Count")
    return table


# Global progress objects used by helper functions.
job_progress = Progress(
    "[progress.description]{task.description}",
    SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    TextColumn("{task.fields[current]}"),
    TimeElapsedColumn(),
)

overall_progress = Progress()
overall_task = overall_progress.add_task("All Jobs", total=0)  # total will be updated below


def setup_jobs() -> None:
    """
    Create progress tasks for each job.
    (Note: the total value for each job is set based on the work expected.)
    """
    # Download comprehensive rules (simulate with total=1)
    job_progress.add_task(
        "[green]Download Rules",
        total=1,
        name="download_comprehensive_rules",
        current=None,
    )
    # Generate catalogs: one task per endpoint.
    job_progress.add_task(
        "[magenta]Generate Catalogs",
        total=len(catalog_endpoints),
        name="generate_catalog_table",
        current=None,
    )
    # Other single-step tasks.
    job_progress.add_task(
        "[magenta]Generate All Cards",
        total=1,
        name="generate_scryfall_all_cards",
        current=None,
    )
    job_progress.add_task(
        "[magenta]Generate Unique Artwork",
        total=1,
        name="generate_scryfall_artwork",
        current=None,
    )
    job_progress.add_task(
        "[magenta]Generate Default Cards",
        total=1,
        name="generate_scryfall_default_cards",
        current=None,
    )
    job_progress.add_task(
        "[magenta]Generate Card Rulings",
        total=1,
        name="generate_scryfall_rulings",
        current=None,
    )
    job_progress.add_task(
        "[magenta]Generate Oracle Cards",
        total=1,
        name="generate_scryfall_oracle",
        current=None,
    )

    # Set the overall total as the sum of all individual tasks
    overall_total = sum(task.total for task in job_progress.tasks)
    overall_progress.update(overall_task, total=overall_total)


def safe_update(job: Progress.TaskID) -> None:
    """
    Try to update the given job task and advance it if not finished.
    Any exception during update is logged.
    """
    try:
        job_progress.update(job.id)
    except Exception:
        console.print_exception()
    if not job.finished:
        job_progress.advance(job.id)


def process_download_rules(job, tbl: Table) -> None:
    """Process the 'download_comprehensive_rules' job."""
    # Set a current status indicator
    job.fields["current"] = "DL"
    tbl.add_row("0", "download_rules", "[green]1-2-3-4-5")
    safe_update(job)


def process_catalogs(job, tbl: Table) -> None:
    """Process the 'generate_catalog_table' job."""
    # For each catalog endpoint, call the function and update the table.
    for idx, endpoint in enumerate(catalog_endpoints):
        job.fields["current"] = endpoint
        try:
            result = generate_catalog_table(table=endpoint)
        except Exception:
            console.print_exception()
            result = "Error"
        tbl.add_row(str(idx), endpoint, f"[green]{result}")
        safe_update(job)


def process_single_step_job(job, tbl: Table, label: str, func) -> None:
    """
    Process a single-step job.
    :param job: The job task.
    :param tbl: The table to update.
    :param label: Label to display in the table.
    :param func: Function to call to get the result.
    """
    job.fields["current"] = "1"
    try:
        result = func()
    except Exception:
        console.print_exception()
        result = "Error"
    tbl.add_row("1", label, f"[green]{result}")
    safe_update(job)


def process_job(job, tbl: Table) -> None:
    """Dispatch job processing based on job name."""
    job_name = job.fields.get("name")
    if job_name == "download_comprehensive_rules":
        process_download_rules(job, tbl)
    elif job_name == "generate_catalog_table":
        process_catalogs(job, tbl)
    elif job_name == "generate_scryfall_all_cards":
        process_single_step_job(job, tbl, "generate_scryfall_all_cards", generate_all_cards_cache)
    elif job_name == "generate_scryfall_artwork":
        process_single_step_job(job, tbl, "generate_scryfall_artwork", generate_unique_artwork_cache)
    elif job_name == "generate_scryfall_default_cards":
        process_single_step_job(job, tbl, "generate_scryfall_default_cards", generate_default_cards_cache)
    elif job_name == "generate_scryfall_rulings":
        process_single_step_job(job, tbl, "generate_scryfall_rulings", generate_card_rulings_cache)
    elif job_name == "generate_scryfall_oracle":
        process_single_step_job(job, tbl, "generate_scryfall_oracle", generate_oracle_cache)
    else:
        console.log(f"[yellow]Unknown job name: {job_name}")


def main() -> None:
    """Main function to set up and run the live progress loop."""
    setup_jobs()

    # Build a layout that shows overall progress and the job details side by side.
    progress_table = Table.grid()
    progress_table.add_row(
        Panel.fit(
            overall_progress,
            title="Overall Progress",
            border_style="green",
            padding=(2, 2),
        ),
        Panel.fit(job_progress, title="[b]Jobs", border_style="red", padding=(1, 2)),
    )

    # Live update loop. The refresh rate is set high so that changes are shown quickly.
    with Live(progress_table, refresh_per_second=100):
        while not overall_progress.finished:
            sleep(0.1)
            # Create a new table for the current cycle.
            tbl = create_table()

            # Process each job in the job_progress.
            for job in job_progress.tasks:
                process_job(job, tbl)

            # Update the overall progress based on the sum of completed work.
            completed = sum(task.completed for task in job_progress.tasks)
            overall_progress.update(overall_task, completed=completed)


if __name__ == "__main__":
    main()
