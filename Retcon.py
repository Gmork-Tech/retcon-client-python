import json

import dynaconf
import websocket
import rel
from dynaconf import Dynaconf, Validator

from model.props import ConfigProp


class Retcon:

    def __init__(self, config_name: str):
        self.__init__(config=Dynaconf(environments=True, env=config_name))

    def __init__(self, config: Dynaconf):

        # Validate the config
        config.validators.register(
            Validator("scheme", default="ws"),
            Validator("host", default="localhost:8080"),
            Validator("scheme", "host", "appId", must_exist=True)
        )

        try:
            config.validators.validate_all()
        except dynaconf.ValidationError as e:
            print(e.details)

        self.config = config
        self.bools: dict[str, list[ConfigProp]] = {}
        self.durations: dict[str, list[ConfigProp]] = {}
        self.lists: dict[str, list[ConfigProp]] = {}
        self.numbers: dict[str, list[ConfigProp]] = {}
        self.objects: dict[str, list[ConfigProp]] = {}
        self.strings: dict[str, list[ConfigProp]] = {}
        self.timestamps: dict[str, list[ConfigProp]] = {}

        url = config.scheme + "://" + config.host + "/ws/" + config.appId

        # Configure the websocket client
        self.ws = websocket.WebSocketApp(url,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

        # Automatically reconnect after 5 seconds if connection closes unexpectedly
        self.ws.run_forever(dispatcher=rel, reconnect=5)
        # Handle interrupts
        rel.signal(2, rel.abort)
        rel.dispatch()

    def apply_properties_from(self, message: any):
        body = json.loads(message)
        if body["deployments"] is not None:
            for deployment in body["deployments"]:
                if deployment["props"] is not None:
                    for prop in deployment["props"]:
                        de_prop = ConfigProp.from_json(prop)

    def on_open(self, ws):
        print("WebSocket connection opened.")

    def on_message(self, ws, message):
        print("Message received:", message)
        self.apply_properties_from(message)

    def on_error(self, ws, error):
        print("WebSocket error:", error)

    def on_close(self, ws, status, message):
        print("WebSocket connection closed.")
