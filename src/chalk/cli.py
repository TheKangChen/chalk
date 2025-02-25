from typing import Required
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


@click.group()
def zoom():
    """Schedule Zoom meetings"""
    pass


@zoom.command()
@click.option("-c", "--class", help="Topic of the meeting (classname).")
@click.option("-D", "--date", required=True, help="Date of meeting.")
@click.option("-t", "--time", help="Start time of the meeting.")
@click.option(
    "-d",
    "--duration",
    type=int,
    help="Duration of the meeting in n times 15 minutes",
)
@click.option(
    "--from-schedule", is_flag=True, help="Creates meeting from config/schedule"
)
def schedule(date, time, length):
    """Schedule Zoom classes."""
    click.echo(f"Scheduling classes on {date} with time {time} for {length} minutes.")


@click.group()
def mail():
    """Manage gmail tasks."""
    pass


@mail.command()
@click.option("-d", "--draft", is_flag=True, help="Draft an email based on template.")
@click.option("-S", "--send", is_flag=True, help="Send an email based on template.")
@click.option("-s", "--schedule", is_flag=True, help="Schedule an email.")
@click.option("--template", required=True, help="Email template to use.")
@click.option("--date", help="Schedule email on this date.")
@click.option("--time", help="Schedule email at this time.")
def email(draft, send, schedule, template, date, time):
    """Handle email operations."""
    if draft:
        click.echo(f"Drafting email using template {template}.")
    elif send:
        click.echo(f"Sending email using template {template}.")
    elif schedule:
        click.echo(f"Scheduling email using template {template} on {date} at {time}.")
    else:
        click.echo("No action specified.")


@click.group()
def cli():
    """Chalk CLI"""
    pass


cli.add_command(zoom)
cli.add_command(mail)
