# system modules
import logging
import functools
import operator
import types
import re

# internal modules

# external modules
import selenium.webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
import click

logger = logging.getLogger(__name__)


def action(description=None):
    """
    Create a decorator to ask before calling a function
    """

    def decorator(decorated_function):
        @functools.wraps(decorated_function)
        def wrapper(self, *args, **kwargs):
            docline = next(
                filter(
                    bool,
                    re.split(
                        r"\s*\n+\s*",
                        getattr(decorated_function, "__doc__", "") or "",
                    ),
                ),
                None,
            )
            actiontext = next(
                filter(bool, filter(bool, (description, docline))),
                decorated_function.__name__,
            )
            if self.interactive:
                while True:
                    proceed = click.prompt(
                        "{}?".format(actiontext),
                        type=click.Choice(("y", "n", "skip", "shell")),
                        default="y",
                    )
                    if proceed.lower() == "y":
                        logger.info("Executing {}".format(repr(actiontext)))
                        return decorated_function(self, *args, **kwargs)
                    elif proceed.lower() == "n":
                        raise click.Abort()
                    elif proceed.lower() == "skip":
                        return
                    elif proceed.lower() == "shell":
                        import IPython

                        client = self

                        IPython.embed(
                            header="The client can be accessed "
                            "via the `client` variable. "
                            "The webdriver instance is "
                            "accessible through `client.webdriver`. "
                            "Run `exit` or press CTRL-D to "
                            "quit the interactive session."
                        )
            logger.info("Executing {}".format(repr(actiontext)))
            return decorated_function(self, *args, **kwargs)

        return wrapper

    return decorator


class Client:
    """
    OpenRepos.net web client
    """

    OPENREPOS_HOMEPAGE = "https://openrepos.net"

    def __init__(self, **kwargs):
        properties = set(
            k for k, v in vars(type(self)).items() if isinstance(v, property)
        )
        for k, v in kwargs.items():
            if k not in properties:
                raise ValueError(
                    "{} has no property {}".format(
                        type(self).__name__, repr(k)
                    )
                )
            setattr(self, k, v)

    @property
    def username(self):
        return getattr(self, "_username", None)

    @username.setter
    def username(self, value):
        setattr(self, "_username", str(value))

    @property
    def password(self):
        return getattr(self, "_password", None)

    @password.setter
    def password(self, value):
        setattr(self, "_password", str(value))

    @property
    def webdriver_class(self):
        return getattr(
            self,
            "_webdriver_class",
            next(self.matching_webdriver(), (WebDriver.__name__, WebDriver))[
                -1
            ],
        )

    @property
    def interactive(self):
        return getattr(self, "_interactive", False)

    @interactive.setter
    def interactive(self, value):
        setattr(self, "_interactive", bool(value))

    @webdriver_class.setter
    def webdriver_class(self, value):
        if not issubclass(value, WebDriver):
            raise ValueError(
                "webdriver_class needs to be a WebDriver, not {}".format(
                    type(value).__name__
                )
            )
        setattr(self, "_webdriver_class", value)

    @property
    def webdriver(self):
        try:
            return self._webdriver
        except AttributeError:
            self._webdriver = self.create_webdriver()
        return self._webdriver

    def execute_action(self, fun, *args, description=None, **kwargs):
        decorator = action(description=description)
        logger.debug("Decorating {} with {}".format(fun, decorator))
        if not isinstance(getattr(fun, "__self__", object), type(self)):
            logger.debug("Converting to methodtype")

            def wrapper(self, *args, **kwargs):
                return fun(*args, **kwargs)

            decorated_function = decorator(wrapper)
        else:
            decorated_function = decorator(fun)
        logger.debug(
            "Calling {} with {}, {}".format(decorated_function, args, kwargs)
        )
        return decorated_function(self, *args, **kwargs)

    @staticmethod
    def matching_webdriver(s=""):
        """
        Generator yielding matching :any:`WebDriver` classes
        """
        for subcls in WebDriver.__subclasses__():
            for name, v in selenium.webdriver.__dict__.items():
                if v is subcls:
                    if s.lower() in v.__name__.lower():
                        yield (name, subcls)

    @action("Open the webdriver")
    def create_webdriver(self):
        """
        Create the webdriver
        """
        logger.debug(
            "Creating {} webdriver".format(
                ".".join(
                    (
                        self.webdriver_class.__module__,
                        self.webdriver_class.__name__,
                    )
                )
            )
        )
        return self.webdriver_class()

    @action()
    def go_to_home_page(self):
        """
        Go to the home page
        """
        self.webdriver.get(self.OPENREPOS_HOMEPAGE)

    @action()
    def go_to_my_apps(self):
        """
        Go to the My Applications page
        """
        try:
            self.webdriver.find_element_by_link_text("My Applications").click()
        except NoSuchElementException:
            logger.debug(
                "Can't find My Applications link. Probably not logged in."
            )
            self.login()
            logger.debug("Retrying to go to My Applications")
            self.webdriver.find_element_by_link_text("My Applications").click()

    @action()
    def go_to_new_app(self):
        """
        Go to Add Application page
        """
        try:
            link = self.webdriver.find_element_by_link_text("Add Application")
            self.execute_action(
                link.click, description="Click Add Aplication link"
            )
        except NoSuchElementException:
            logger.debug(
                "Can't find Add Application link. Probably not logged in."
            )
            self.login()
            logger.debug("Retrying to go to New Application")
            link = self.webdriver.find_element_by_link_text("Add Application")
            self.execute_action(
                link.click, description="Click Add Aplication link"
            )

    @action()
    def new_app(self, name, platform, category):
        """
        Create a new app
        """
        self.go_to_new_app()
        links = self.webdriver.find_elements_by_xpath(
            "//div[@id='block-system-main']//a"
        )
        try:
            link = next(
                filter(
                    lambda e: re.match(r"(.*?)\s+Application$", e.text)
                    and platform.lower() in e.text.lower(),
                    links,
                )
            )
        except (StopIteration, NoSuchElementException):
            raise click.UsageError(
                "Can't find link for platform {}. "
                "Possible values are {}".format(
                    repr(platform),
                    ", ".join(
                        map(
                            repr,
                            map(
                                operator.methodcaller("group", 1),
                                filter(
                                    bool,
                                    map(
                                        lambda e: re.match(
                                            r"(.*?)\s+Application$", e.text
                                        ),
                                        links,
                                    ),
                                ),
                            ),
                        )
                    ),
                )
            )
        self.execute_action(
            link.click, description="Click {} link".format(repr(link.text))
        )
        title_field = self.webdriver.find_element_by_id("edit-title")
        self.execute_action(
            title_field.send_keys,
            name,
            description="Enter {} title".format(repr(name)),
        )
        category_menu = Select(
            self.webdriver.find_element_by_id(
                "edit-field-category-und-hierarchical-select-selects-0"
            )
        )
        try:
            index = next(
                (
                    i
                    for i, e in enumerate(category_menu.options)
                    if (
                        category.lower() in e.text.lower()
                        and "none" not in e.text.lower()
                    )
                )
            )
        except StopIteration:
            raise click.UsageError(
                "No such category {}. "
                "Possible selections include {}".format(
                    repr(category),
                    ", ".join(
                        map(
                            repr,
                            map(
                                operator.methodcaller("group", 1),
                                filter(
                                    bool,
                                    map(
                                        lambda e: re.match(
                                            r"(?!<)(.*?)\s*(?:\(\d+\))?$",
                                            e.text,
                                        ),
                                        category_menu.options,
                                    ),
                                ),
                            ),
                        )
                    ),
                )
            )
        self.execute_action(
            category_menu.select_by_index,
            index,
            description="Select category {}".format(
                repr(category_menu.options[index].text)
            ),
        )
        save_button = self.webdriver.find_element_by_id("edit-submit--2")
        self.execute_action(save_button.click, description="Click Save button")

    @action()
    def login(self, username=None, password=None):
        """
        Log in to the account
        """
        if self.webdriver.current_url != self.OPENREPOS_HOMEPAGE:
            self.go_to_home_page()

        if not username:
            username = self.username
        if not password:
            password = self.password

        if not (username and password):
            raise ValueError("Both username and password must be specified!")

        username_field = self.webdriver.find_element_by_id("edit-name")
        self.execute_action(
            username_field.send_keys, username, description="Type username"
        )

        password_field = self.webdriver.find_element_by_id("edit-pass")
        self.execute_action(
            password_field.send_keys, password, description="Type password"
        )

        login_button = self.webdriver.find_element_by_id("edit-submit--3")
        self.execute_action(
            login_button.click, description="Click Login Button"
        )

    @action()
    def close(self):
        """
        Close the webdriver
        """
        if getattr(self, "_webdriver", None):
            self._webdriver.close()
            del self._webdriver

    def __del__(self):
        self.interactive = False
        if getattr(self, "_webdriver", None):
            self.close()
