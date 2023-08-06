# system modules
import logging

# internal modules
from openrepos.cli.commands.main import cli

# external modules
import click

logger = logging.getLogger(__name__)


@cli.command(help="Go the the OpenRepos.net home page")
@click.pass_obj
def home(obj):
    logger.info("Going to the OpenRepos.net homepage")
    obj["client"].go_to_home_page()
    logger.debug(
        "Homepage title is {}".format(repr(obj["client"].webdriver.title))
    )


@cli.command(help="Go the My Applications page")
@click.pass_obj
def my_apps(obj):
    logger.info("Going to the My Applications page")
    obj["client"].go_to_my_apps()


@cli.command(help="Log in to an account")
@click.option(
    "-u",
    "--username",
    metavar="USERNAME",
    help="OpenRepos.net username",
    show_envvar=True,
)
@click.option(
    "-p",
    "--password",
    metavar="PASSWORD",
    help="OpenRepos.net password",
    show_envvar=True,
)
@click.pass_obj
def login(obj, username, password):
    logger.info("Logging in")
    obj["client"].login(username, password)


@cli.command(help="Create a new app")
@click.option(
    "-n",
    "--name",
    metavar="APPNAME",
    help="name for the new app",
    required=True,
    show_envvar=True,
)
@click.option(
    "-p",
    "--platform",
    metavar="PLATFORM",
    help="which platform to create the app for. At the time of writing, "
    "possible selections were {}".format(
        ", ".join(("SailfishOS", "NemoMobile", "Harmattan", "Maemo"))
    ),
    required=True,
    show_envvar=True,
)
@click.option(
    "-c",
    "--category",
    metavar="CATEGORY",
    help="which category to choose for the app. At the time of writing, "
    "possible selections were {}".format(
        ", ".join(("Coding Competition", "Applications", "Games", "Libraries"))
    ),
    required=True,
    show_envvar=True,
)
@click.pass_obj
def new_app(obj, name, platform, category):
    obj["client"].new_app(name=name, platform=platform, category=category)
