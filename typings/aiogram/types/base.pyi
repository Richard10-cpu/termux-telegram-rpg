from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

from aiogram.client.context_controller import BotContextController
from aiogram.client.default import Default


class TelegramObject(BotContextController, BaseModel):
    model_config: ConfigDict

    @classmethod
    def remove_unset(cls, values: dict[str, Any]) -> dict[str, Any]: ...


class MutableTelegramObject(TelegramObject):
    model_config: ConfigDict


class UNSET_TYPE: ...


UNSET: UNSET_TYPE
UNSET_PARSE_MODE: Default
UNSET_DISABLE_WEB_PAGE_PREVIEW: Default
UNSET_PROTECT_CONTENT: Default
