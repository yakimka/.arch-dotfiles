from dataclasses import dataclass
from enum import Enum
from typing import Optional

from wmtools.core.command import CommandMixin


class ShowType(str, Enum):
    run = 'run'
    drun = 'drun'
    dmenu = 'dmenu'


@dataclass
class WofiCommand(CommandMixin):
    BASE_ARGS = ('wofi',)

    dmenu: Optional[bool] = None
    show: Optional[ShowType] = None
    prompt: Optional[str] = None
    lines: Optional[int] = None
    columns: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    location: Optional[int] = None
    xoffset: Optional[int] = None
    yoffset: Optional[int] = None
    allow_markup: Optional[bool] = None
    no_actions: Optional[bool] = None
    insensitive: Optional[bool] = None
    allow_images: Optional[bool] = None
    image_size: Optional[int] = None
    gtk_dark: Optional[bool] = None
    cache_file: Optional[str] = None
    password: Optional[str] = None
    conf: Optional[str] = None
    style: Optional[str] = None
