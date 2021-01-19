"""
pygame-menu
https://github.com/ppizarror/pygame-menu

PYGAME-MENU
A menu for pygame, simple, lightweight and easy to use.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2021 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

"""
BaseImage: Provides basic image loading an manipulation with pygame
"""
# noinspection PyUnresolvedReferences
import pygame_menu.baseimage

"""
Controls: Default controls of menu object and key definition
"""
# noinspection PyUnresolvedReferences
import pygame_menu.controls

"""
Events: Menu events definition and locals
"""
# noinspection PyUnresolvedReferences
import pygame_menu.events

"""
Fonts: Menu fonts
"""
# noinspection PyUnresolvedReferences
import pygame_menu.font

"""
Locals: Local constants
"""
# noinspection PyUnresolvedReferences
import pygame_menu.locals

"""
ScrollArea: Scrollarea class
"""
# noinspection PyUnresolvedReferences
import pygame_menu.scrollarea

"""
Sound: Sound class
"""
# noinspection PyUnresolvedReferences
import pygame_menu.sound

"""
Themes: Menu themes class
"""
# noinspection PyUnresolvedReferences
import pygame_menu.themes

"""
Version: Library version
"""
# noinspection PyUnresolvedReferences
import pygame_menu.version

"""
Widgets: Menu widgets
"""
import pygame_menu.widgets

"""
Menu: Menu class
"""
# noinspection PyUnresolvedReferences
from pygame_menu.menu import Menu

"""
Metadata: Information about the project
"""
__author__ = 'ppizarror'
__contributors__ = [
    'anxuae',
    'arpruss',
    'asierrayk',
    'DA820',
    'eforgacs',
    'i96751414',
    'ironsmile',
    'jwllee',
    'maditnerd',
    'notrurs',
    'NullP01nt',
    'PandaRoux8',
    'ppizarror',
    'Rifqi31',
    'thisIsMikeKane',
    'werdeil',
    'zPaw'
]
__copyright__ = 'Copyright 2017-2021 Pablo Pizarro R. @ppizarror'
__description__ = 'A menu for pygame, simple, lightweight and easy to use'
__email__ = 'pablo@ppizarror.com'
__keywords__ = 'pygame menu menus gui widget input button pygame-menu'
__license__ = 'MIT'
__url__ = 'https://pygame-menu.readthedocs.io/en/latest/'
__url_source_code__ = 'https://github.com/ppizarror/pygame-menu/tree/master/pygame_menu'
__url_documentation__ = 'https://pygame-menu.readthedocs.io/en/latest/'
__url_bug_tracker__ = 'https://github.com/ppizarror/pygame-menu/issues'
__version__ = pygame_menu.version.ver
