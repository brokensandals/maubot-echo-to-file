from typing import Type
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from maubot import Plugin, MessageEvent
from maubot.handlers import event
from mautrix.types import EventType, MessageEvent, MediaMessageEventContent
from mautrix.types.event.message import BaseFileInfo, MessageType
from mautrix.crypto.attachments import decrypt_attachment
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from mimetypes import guess_extension


class Config(BaseProxyConfig):
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("allowlist")
        helper.copy("output_file")
        helper.copy("attachment_dir")


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
        outfile_path = Path(self.config["output_file"])

        # TODO use origin timestamp instead
        ts = datetime.now(timezone.utc).astimezone()
        entry = evt.content.body

        if isinstance(evt.content, MediaMessageEventContent):
            outfile_dir = outfile_path.parent
            attachments_path = Path(self.config["attachment_dir"])

            fileid = uuid4()
            filename = str(fileid)
            if isinstance(evt.content.info, BaseFileInfo) and evt.content.info.mimetype:
                ext = guess_extension(evt.content.info.mimetype)
                if ext:
                    filename += ext
            
            filepath = attachments_path.joinpath(filename)

            data = None
            if evt.content.url:
                data = await self.client.download_media(evt.content.url)
            elif evt.content.file and evt.content.file.url:
                ciphertext = await self.client.download_media(evt.content.file.url)
                data = decrypt_attachment(ciphertext, evt.content.file.key.key, evt.content.file.hashes["sha256"], evt.content.file.iv)
            
            if data is not None:
                filepath.write_bytes(data)
                entry = ""
                if evt.content.msgtype == MessageType.IMAGE:
                    entry = "!"
                # TODO escaping
                entry += f"[{evt.content.body}]({filepath.relative_to(outfile_dir)})"
                
        
        text = f"{ts.strftime('%Y-%m-%d %H:%M')}: {entry}\n\n"

        with open(self.config["output_file"], "a") as outfile:
            outfile.write(text)
        await evt.mark_read()

