from pathlib import Path
from typing import Dict, List, Type

from mycroft_bus_client import Message
from selenium import webdriver

from ..base import Action
from .handlers.base import Handler
from .handlers.selector import SelectionHandler


class BrowserAction(Action):

    HOME_URL = (Path(__file__).parent / "index.html").absolute().as_uri()

    def __init__(self):

        super().__init__()

        self.driver = self.get_driver()

        self.cleanup()  # Default to the home page

        self.is_noisy = False
        self.logger.info(
            "Browser is ready with the following handlers: %s",
            ", ".join(
                [
                    c.__name__.replace("Handler", "")
                    for c in self.get_handlers()
                ]
            ),
        )

    def get_driver(self) -> webdriver.Chrome:

        self.logger.info("Setting up browser")

        options = webdriver.ChromeOptions()
        options.add_argument("disable-infobars")
        options.add_argument("--start-fullscreen")
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )
        options.add_argument(
            "--user-data-dir={}/.config/chromium".format(Path.home())
        )

        return webdriver.Chrome(options=options)

    def get_message_types(self) -> Dict[str, callable]:
        return {
            "skill.majel.browser.open": self.handle_single,
            "skill.majel.browser.open-selector": self.handle_multiple,
            "skill.majel.browser.stop": self.handle_stop,
        }

    @staticmethod
    def get_handlers() -> List[Type[Handler]]:
        return sorted(Handler.__subclasses__(), key=lambda c: c.PRIORITY)

    def get_handler(self, payload: str) -> Handler:
        """
        Using the message contents, ask each handler if it can in fact handle
        it.  If it says it can, return an instance of that handler.
        """
        for handler in self.get_handlers():
            self.logger.info("Checking if %s can handle %s", handler, payload)
            if handler := handler.build_from_payload(self.driver, payload):
                self.logger.info("OK: %s can handle %s", handler, payload)
                return handler

    def handle_single(self, message: Message) -> None:
        self.logger.info(str(message.data))
        handler = self.get_handler(message.data.get("url"))
        self.is_noisy = handler.handle()

    def handle_multiple(self, message: Message) -> None:
        handler = SelectionHandler(self.driver, message.data.get("urls"))
        self.is_noisy = handler.handle()

    def handle_stop(self, *args) -> None:
        if self.is_noisy:
            self.cleanup()

    def cleanup(self) -> None:
        self.is_noisy = False
        self.driver.get(self.HOME_URL)
