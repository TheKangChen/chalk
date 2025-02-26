import click

import pathlib

CONFIG_DIR = pathlib.Path(__file__).parent.parent.parent / "config"

EMAIL_TEMPLATES_DIR = CONFIG_DIR / "email_templates"
SECRETS_DIR = CONFIG_DIR / "secrets"


def validate_date():
    """Validate date in command to match 'YYYY-MM-DD' format"""
    raise


def validate_time():
    """Validate time in command to match 'HH:MM' format. Step size 15 mins"""
    raise


def validate_duration():
    """Validate duration in command. Step size 15 mins"""
    raise


# -------------------------------
# CLI Entry Point
# -------------------------------


@click.group()
def cli():
    """Chalk - TechConnect CLI automation tool."""
    pass


# -------------------------------
# Zoom Commands
# -------------------------------


@cli.group()
def zoom():
    """Manage Zoom meetings."""
    pass


@zoom.command(context_settings={"ignore_unknown_options": True})
@click.argument("topic", required=True, type=str)
@click.option("-d", "--date", required=True, help="Schedule meeting date.")
@click.option("-t", "--time", required=True, help="Specify meeting start time.")
@click.option(
    "-D",
    "--duration",
    required=True,
    type=int,
    help="Duration of the meeting in n times 15 minutes.",
)
@click.option(
    "--from-schedule",
    is_flag=True,
    help="Create meetings from config/schedule, --month or --date argument required.",
)
@click.option(
    "-m", "--month", help="Create meetings of this month, used with --from-schedule."
)
@click.option(
    "-h",
    "--headless-mode",
    is_flag=True,
    default=False,
    help="Use Playwright in headless mode.",
)
def create(topic, date, time, duration, from_schedule, month, headless_mode):
    """(Not implemented) Create a Zoom meeting with a topic."""
    if from_schedule:
        if not month and not date:
            raise click.UsageError(
                "--from-schedule flag requires --month or --date argument."
            )
        if month:
            click.echo(f"Creating Zoom meetings for {month} from schedule.")
        if date:
            click.echo(f"Creating Zoom meetings on {date} from schedule.")
    else:
        click.echo(
            f"Creating Zoom meeting: '{topic}' on {date} at {time} for {duration} minutes. (schedule?: {from_schedule}, headless-mode?: {headless_mode})"
        )


# -------------------------------
# Gmail Commands TODO:
# -------------------------------


@cli.group()
def mail():
    """Manage Gmail tasks."""
    pass


@mail.command(context_settings={"ignore_unknown_options": True})
@click.option("-T", "--template", required=True, help="Email template to use.")
def draft(template):
    """(Not implemented) Draft an email using a template."""
    click.echo(f"Drafting email using template {template}.")


@mail.command(context_settings={"ignore_unknown_options": True})
@click.option("-T", "--template", required=True, help="Email template to use.")
def send(template):
    """(Not implemented) Send an email using a template."""
    click.echo(f"Sending email using template {template}.")


@mail.command(context_settings={"ignore_unknown_options": True})
@click.option("-T", "--template", required=True, help="Email template to use.")
@click.option("-d", "--date", required=True, help="Schedule email on this date.")
@click.option("-t", "--time", required=True, help="Schedule email at this time.")
def schedule(template, date, time):
    """(Not implemented) Schedule an email to be sent later."""
    click.echo(f"Scheduling email using template {template} on {date} at {time}.")


# -------------------------------
# Google Calendar Commands TODO:
# -------------------------------


@cli.group()
def calendar():
    """Manage Google Calendar events."""
    pass


@calendar.command(context_settings={"ignore_unknown_options": True})
@click.argument("event-topic", required=True, type=str)
@click.option("-d", "--date", required=True, help="Create calendar event on this date.")
@click.option("-t", "--time", required=True, help="Create calendar event at this time.")
def create(event_topic, date, time):
    """(Not implemented) Create calendar event."""
    click.echo(f"Creating calendar event '{event_topic}' on {date} at {time}.")


@calendar.command(context_settings={"ignore_unknown_options": True})
@click.option("-d", "--date", help="Create calendar event on this date.")
@click.option("-t", "--time", help="Create calendar event at this time.")
@click.option("-a", "--all", is_flag=True, help="Create all events from schedule.")
def create_from_schedule(date, time, all):
    """(Not implemented) Create calendar events from schedule."""
    click.echo(f"Creating events on {date} at {time}. (all?: {all})")


# -------------------------------
# Drupal Event Commands TODO:
# -------------------------------


@cli.group()
def classes():
    """Manage Drupal events."""
    pass


@classes.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "-d", "--date", required=True, help="Get registration emails of class on this date."
)
@click.option(
    "-t", "--time", required=True, help="Get registration emails of class at this time."
)
def get_registration(date, time):
    """(Not implemented) Get registration emails."""
    click.echo(f"Getting registration emails of class on {date} at {time}.")


@classes.command(context_settings={"ignore_unknown_options": True})
@click.option("-d", "--date", help="Create class on this date.")
@click.option("-t", "--time", help="Create class at this time.")
@click.option(
    "--from-schedule",
    is_flag=True,
    help="Create events from schedule, --month argument required.",
)
@click.option(
    "-m",
    "--month",
    help="Create all drupal events of this month, used with --from-schedule.",
)
def create(date, time, from_schedule, month):
    """(Not implemented) Create Drupal event."""
    if from_schedule:
        if not month:
            raise click.UsageError("--from_schedule flag requires --month argument.")
        click.echo(f"Creating Drupal event of {month}.")
    else:
        click.echo(f"Creating Drupal events on {date} at {time}.")


# -------------------------------
# Pipeline Commands TODO:
# -------------------------------


@cli.group()
def pipeline():
    """Automation pipelines. Requires a schedule."""
    pass


@pipeline.command(context_settings={"ignore_unknown_options": True})
@click.option("-d", "--date", required=True, help="Schedule meeting date.")
@click.option("-t", "--time", required=True, help="Specify meeting start time.")
@click.option("-T", "--template", required=True, help="Email template to use.")
def schedule_and_email_one(date, time, template):
    """(Not implemented) Scheule Zoom meeting and draft email with template and registration list (if available) for one class."""
    click.echo(
        f"Schedule meeting at {date} {time} and creating email draft with {template}."
    )


@pipeline.command(context_settings={"ignore_unknown_options": True})
@click.option("-d", "--dates", required=True, type=list, help="Schedule meeting date.")
@click.option("-T", "--template", required=True, help="Email template to use.")
def schedule_and_email_many(dates, template):
    """(Not implemented) Scheule Zoom meetings and draft emails with template and registration list (if available) for multiple classes."""
    click.echo(
        f"Schedule meetings for {dates} and creating email drafts with {template}."
    )


@pipeline.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "-D", "--dates", type=list, help="Create drupal and calendar events for dates."
)
@click.option("-d", "--date", help="Create drupal and calendar event for this date.")
@click.option("-t", "--time", help="Create drupal and calendar event for this time.")
def drupal_and_calendar(dates, date, time):
    """(Not implemented) Create Drupal and Calender event(s)."""
    if dates:
        click.echo(f"Creating Drupal and Calendar events for {dates}.")
    else:
        if date and time:
            click.echo(f"Creating Drupal and Calendar event at {date} {time}.")
        else:
            raise click.UsageError(
                "--date and --time arguments are both required when creating singular event."
            )


@pipeline.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "-D",
    "--dates",
    type=list,
    help="Create drupal, calendar, and zoom events for dates.",
)
@click.option(
    "-d", "--date", help="Create drupal, calendar, and zoom event for this date."
)
@click.option(
    "-t", "--time", help="Create drupal, calendar, and zoom event for this time."
)
def drupal_and_calendar_and_zoom(dates, date, time):
    """(Not implemented) Create Drupal, Calender, and Zoom event(s)."""
    if dates:
        click.echo(f"Creating Drupal, Calender, and Zoom events for {dates}.")
    else:
        if date and time:
            click.echo(f"Creating Drupal, Calender, and Zoom event at {date} {time}.")
        else:
            raise click.UsageError(
                "--date and --time arguments are both required when creating singular event."
            )
