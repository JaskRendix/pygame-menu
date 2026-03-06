"""
pygame-menu
https://github.com/ppizarror/pygame-menu

PYGAME-MENU
A menu for pygame. Simple, and easy to use.
"""

import os
from importlib.metadata import PackageNotFoundError, metadata

__all__ = ["BaseImage", "Menu", "Sound", "Theme"]

# Metadata
try:
    _meta = metadata("pygame-menu")
    __version__ = _meta.get("Version")
    __author__ = _meta.get("Author")
    __email__ = _meta.get("Author-email")
    __description__ = _meta.get("Summary")
    __license__ = _meta.get("License")
    __url__ = _meta.get("Home-page")
    __module_name__ = _meta.get("Name")
except PackageNotFoundError:
    # Local fallback
    __version__ = "4.4.3"
    __author__ = "Pablo Pizarro R."
    __email__ = "pablo@ppizarror.com"
    __description__ = "A menu for pygame. Simple, and easy to use"
    __license__ = "MIT"
    __url__ = "https://pygame-menu.readthedocs.io"
    __module_name__ = "pygame-menu"

# Extra metadata not provided by importlib
__url_documentation__ = "https://pygame-menu.readthedocs.io"
__url_source_code__ = "https://github.com/ppizarror/pygame-menu"
__url_bug_tracker__ = "https://github.com/ppizarror/pygame-menu/issues"
__keywords__ = "pygame menu menus gui widget input button pygame-menu image sound ui"

__contributors__ = [
    "ppizarror",
    "anxuae",
    "apuly",
    "arpruss",
    "asierrayk",
    "DA820",
    "eforgacs",
    "i96751414",
    "ironsmile",
    "jwllee",
    "maditnerd",
    "MayuSakurai",
    "mrkprdo",
    "neilsimp1",
    "notrurs",
    "NullP01nt",
    "PandaRoux8",
    "Rifqi31",
    "ThePeeps191",
    "thisIsMikeKane",
    "vnmabus",
    "werdeil",
    "zPaw",
]

# Pygame check
__pygame_version__ = None
try:
    from pygame import version as __pv

    __pygame_version__ = __pv.vernum
except Exception:
    pass

# Conditional imports
if __pygame_version__ is not None:
    import pygame_menu._scrollarea
    import pygame_menu.baseimage
    import pygame_menu.controls
    import pygame_menu.events
    import pygame_menu.font
    import pygame_menu.locals
    import pygame_menu.menu
    import pygame_menu.sound
    import pygame_menu.themes
    import pygame_menu.widgets
    from pygame_menu.baseimage import BaseImage
    from pygame_menu.menu import Menu
    from pygame_menu.sound import Sound
    from pygame_menu.themes import Theme

# Version print
if (
    "PYGAME_MENU_HIDE_VERSION" not in os.environ
    and "PYGAME_HIDE_SUPPORT_PROMPT" not in os.environ
):
    print(f"{__module_name__} {__version__}")
