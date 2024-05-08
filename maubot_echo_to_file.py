from typing import Type
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from maubot import Plugin, MessageEvent
from maubot.handlers import event
from mautrix.types import EventType, MessageEvent
from datetime import datetime, timezone


class Config(BaseProxyConfig):
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("allowlist")
        helper.copy("output_file")


class EchoToFileBot(Plugin):
    async def start(self) -> None:
        self.config.load_and_update()
    
    def is_allowed(self, sender: str) -> bool:
        if self.config["allowlist"] == False:
            return True
        return sender in self.config["allowlist"]

    @classmethod
    def get_config_class(cls) -> Type[BaseProxyConfig]:
        return Config

    @event.on(EventType.ROOM_MESSAGE)
    async def handle_msg(self, evt: MessageEvent) -> None:
        if not self.is_allowed(evt.sender):
            self.log.warn(f"stranger danger: sender={evt.sender}")
            return
        with open(self.config["output_file"], "a") as outfile:
            # TODO use origin timestamp instead
            ts = datetime.now(timezone.utc).astimezone()
            outfile.write(ts.strftime("%Y-%m-%d %H:%M"))
            outfile.write(": ")
            outfile.write(evt.content.body)
            outfile.write("\n\n")
        await evt.mark_read()

