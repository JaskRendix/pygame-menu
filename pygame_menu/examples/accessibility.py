"""
pygame-menu

EXAMPLE - ACCESSIBILITY AUDIT
Run a WCAG accessibility audit against the current theme.
"""

from __future__ import annotations

import pygame_menu
from pygame_menu.examples import create_example_window

surface = create_example_window(
    "Example - Accessibility Audit",
    (800, 600),
)

menu = pygame_menu.Menu(
    width=600,
    height=450,
    title="Accessibility Audit",
    theme=pygame_menu.themes.THEME_BLUE,
)


def run_aa_audit() -> None:
    """
    Run a WCAG AA audit and display the results.
    """
    report = menu.get_theme().audit_accessibility("AA")

    print("\n" + "=" * 50)
    print(report)


def run_aaa_audit() -> None:
    """
    Run a WCAG AAA audit and display the results.
    """
    report = menu.get_theme().audit_accessibility("AAA")

    print("\n" + "=" * 50)
    print(report)


menu.add.vertical_margin(20)

menu.add.button("Run AA Audit", run_aa_audit)
menu.add.button("Run AAA Audit", run_aaa_audit)

menu.add.vertical_margin(20)

menu.add.button("Quit", pygame_menu.events.EXIT)

if __name__ == "__main__":
    menu.mainloop(surface)
