"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST ACCESSIBILITY
Test Accessibility.
"""

import pygame
import pytest

from pygame_menu.accessibility import (
    AccessibilityCheck,
    AccessibilityReport,
    audit_theme,
    contrast_ratio,
    relative_luminance,
)
from pygame_menu.baseimage import BaseImage
from pygame_menu.themes import (
    THEME_BLUE,
    THEME_DARK,
    THEME_DEFAULT,
    THEME_GREEN,
    THEME_ORANGE,
    THEME_SOLARIZED,
    Theme,
)


def test_invalid_level():
    with pytest.raises(ValueError):
        THEME_DARK.audit_accessibility("INVALID")


def test_relative_luminance_black():
    assert relative_luminance((0, 0, 0)) == 0


def test_relative_luminance_white():
    assert relative_luminance((255, 255, 255)) == 1


def test_contrast_ratio_black_white():
    ratio = contrast_ratio(
        (0, 0, 0),
        (255, 255, 255),
    )

    assert round(ratio, 1) == 21.0


def test_contrast_ratio_is_symmetric():
    a = contrast_ratio(
        (255, 255, 255),
        (0, 0, 0),
    )

    b = contrast_ratio(
        (0, 0, 0),
        (255, 255, 255),
    )

    assert a == b


def test_same_color_contrast_ratio():
    ratio = contrast_ratio(
        (100, 100, 100),
        (100, 100, 100),
    )

    assert ratio == 1.0


def test_accessibility_check_passed():
    check = AccessibilityCheck(
        id="x",
        title="X",
        status="pass",
        severity="info",
        message="ok",
    )

    assert check.passed


def test_accessibility_check_failed():
    check = AccessibilityCheck(
        id="x",
        title="X",
        status="fail",
        severity="info",
        message="ok",
    )

    assert not check.passed


def test_report_summary_counts():
    report = AccessibilityReport(
        level="AA",
        score=0,
        passed=False,
        checks=[
            AccessibilityCheck(
                "a",
                "A",
                "fail",
                "error",
                "",
            ),
            AccessibilityCheck(
                "b",
                "B",
                "fail",
                "warning",
                "",
            ),
            AccessibilityCheck(
                "c",
                "C",
                "fail",
                "info",
                "",
            ),
        ],
    )

    summary = report.summary

    assert summary.errors == 1
    assert summary.warnings == 1
    assert summary.infos == 1


def test_report_to_dict():
    report = THEME_DARK.audit_accessibility()

    d = report.to_dict()

    assert "level" in d
    assert "score" in d
    assert "checks" in d


def test_report_string_generation():
    report = THEME_DARK.audit_accessibility()

    text = str(report)

    assert "Accessibility Audit" in text
    assert "Score" in text


def test_audit_returns_report():
    report = THEME_DARK.audit_accessibility()

    assert isinstance(report, AccessibilityReport)


def test_audit_level_is_normalized():
    report = THEME_DARK.audit_accessibility("aa")

    assert report.level == "AA"


def test_audit_contains_expected_checks():
    report = THEME_DARK.audit_accessibility()

    ids = {c.id for c in report.checks}

    assert "title_contrast" in ids
    assert "widget_contrast" in ids
    assert "selection_visibility" in ids
    assert "focus_visibility" in ids
    assert "readonly_visibility" in ids
    assert "scrollbar_visibility" in ids


def test_bad_widget_contrast_fails():
    theme = Theme(
        background_color=(0, 0, 0),
        widget_font_color=(10, 10, 10),
    )

    report = audit_theme(theme)

    widget_check = next(c for c in report.checks if c.id == "widget_contrast")

    assert widget_check.status == "fail"


def test_bad_title_contrast_fails():
    theme = Theme(
        title_background_color=(0, 0, 0),
        title_font_color=(5, 5, 5),
    )

    report = audit_theme(theme)

    title_check = next(c for c in report.checks if c.id == "title_contrast")

    assert title_check.status == "fail"


def test_failing_error_check_makes_report_fail():
    theme = Theme(
        background_color=(0, 0, 0),
        widget_font_color=(5, 5, 5),
    )

    report = audit_theme(theme)

    assert not report.passed


def test_aaa_not_more_permissive_than_aa():
    theme = Theme(
        background_color=(255, 255, 255),
        widget_font_color=(120, 120, 120),
    )

    aa = theme.audit_accessibility("AA")
    aaa = theme.audit_accessibility("AAA")

    assert aaa.score <= aa.score


def test_default_theme_audits():
    report = THEME_DEFAULT.audit_accessibility()

    assert isinstance(report, AccessibilityReport)


def test_dark_theme_audits():
    report = THEME_DARK.audit_accessibility()

    assert isinstance(report, AccessibilityReport)


def test_blue_theme_audits():
    report = THEME_BLUE.audit_accessibility()

    assert isinstance(report, AccessibilityReport)


def test_green_theme_audits():
    report = THEME_GREEN.audit_accessibility()

    assert isinstance(report, AccessibilityReport)


def test_orange_theme_audits():
    report = THEME_ORANGE.audit_accessibility()

    assert isinstance(report, AccessibilityReport)


def test_solarized_theme_audits():
    report = THEME_SOLARIZED.audit_accessibility()

    assert isinstance(report, AccessibilityReport)


def test_score_never_negative():
    theme = Theme(
        background_color=(0, 0, 0),
        widget_font_color=(0, 0, 0),
        title_background_color=(0, 0, 0),
        title_font_color=(0, 0, 0),
        selection_color=(0, 0, 0),
        readonly_color=(0, 0, 0),
        scrollbar_color=(0, 0, 0),
        scrollbar_slider_color=(0, 0, 0),
    )

    report = audit_theme(theme)

    assert report.score >= 0


def test_score_never_exceeds_100():
    report = THEME_DARK.audit_accessibility()

    assert report.score <= 100


def test_report_string_contains_score():
    report = THEME_DARK.audit_accessibility()

    text = str(report)

    assert "Score:" in text
    assert "Result:" in text


def test_widget_background_baseimage():
    surface = pygame.Surface((10, 10))
    surface.fill((255, 255, 255))

    image = BaseImage(surface)

    theme = Theme(
        widget_background_color=image,
        widget_font_color=(0, 0, 0),
    )

    report = audit_theme(theme)

    assert isinstance(report, AccessibilityReport)


def test_representative_color_single_color():
    surface = pygame.Surface((8, 8))
    surface.fill((255, 0, 0))

    image = BaseImage(surface)

    assert image.get_representative_color() == (255, 0, 0)


def test_report_summary_passed():
    report = AccessibilityReport(
        level="AA",
        score=100,
        passed=True,
        checks=[],
    )

    assert report.summary.passed


def test_report_to_dict_contains_values():
    report = THEME_DARK.audit_accessibility()

    data = report.to_dict()

    assert data["level"] == report.level
    assert data["score"] == report.score
    assert data["passed"] == report.passed


def test_large_text_uses_lower_threshold():
    theme = Theme(
        widget_font_size=24,
        background_color=(255, 255, 255),
        widget_font_color=(120, 120, 120),
    )

    report = audit_theme(theme, "AA")

    assert isinstance(report, AccessibilityReport)


def test_warning_does_not_fail_report():
    report = AccessibilityReport(
        level="AA",
        score=90,
        passed=True,
        checks=[
            AccessibilityCheck(
                "warning",
                "Warning",
                "fail",
                "warning",
                "",
            )
        ],
    )

    assert report.passed


def test_empty_report_summary():
    report = AccessibilityReport(
        level="AA",
        score=100,
        passed=True,
        checks=[],
    )

    summary = report.summary

    assert summary.errors == 0
    assert summary.warnings == 0
    assert summary.infos == 0


def test_representative_color_sampling():
    surface = pygame.Surface((8, 8))

    for x in range(8):
        for y in range(8):
            surface.set_at((x, y), (255, 0, 0))

    image = BaseImage(surface)

    assert image.get_representative_color() == (255, 0, 0)
