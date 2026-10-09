"""
pygame_menu.accessibility

WCAG accessibility audit utilities for Theme objects.
"""

from __future__ import annotations

__all__ = (
    "AccessibilityCheck",
    "AccessibilitySummary",
    "AccessibilityReport",
    "relative_luminance",
    "contrast_ratio",
    "audit_theme",
    "Severity",
    "Status",
)

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Literal

from pygame_menu.baseimage import BaseImage

if TYPE_CHECKING:
    from pygame_menu._types import ColorType, NumberType
    from pygame_menu.themes import Theme

Severity = Literal["error", "warning", "info"]
Status = Literal["pass", "fail"]


@dataclass
class AccessibilityCheck:
    """
    Result of a single accessibility check.

    Stores the outcome, severity and additional information
    related to a specific audit rule.
    """

    id: str
    title: str
    status: Status
    severity: Severity
    message: str
    current_value: Any = None
    suggested_value: Any | None = None

    @property
    def passed(self) -> bool:
        """
        Return ``True`` if the check passed.
        """
        return self.status == "pass"


@dataclass
class AccessibilitySummary:
    """
    Aggregate accessibility audit results.

    Contains the number of failed checks grouped by severity.
    """

    passed: bool
    errors: int
    warnings: int
    infos: int


@dataclass
class AccessibilityReport:
    """
    Accessibility audit report.

    Stores all generated checks together with the overall
    audit score and pass status.
    """

    level: str
    score: int
    passed: bool
    checks: list[AccessibilityCheck] = field(default_factory=list)

    @property
    def summary(self) -> AccessibilitySummary:
        """
        Return a summary of failed checks grouped by severity.
        """
        errors = 0
        warnings = 0
        infos = 0

        for check in self.checks:
            if check.status == "fail":
                if check.severity == "error":
                    errors += 1
                elif check.severity == "warning":
                    warnings += 1
                else:
                    infos += 1

        return AccessibilitySummary(
            passed=self.passed,
            errors=errors,
            warnings=warnings,
            infos=infos,
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Export the report as a serializable dictionary.

        :return: Report data
        """
        summary = self.summary

        return {
            "level": self.level,
            "score": self.score,
            "passed": self.passed,
            "summary": {
                "passed": summary.passed,
                "errors": summary.errors,
                "warnings": summary.warnings,
                "infos": summary.infos,
            },
            "checks": [
                {
                    "id": c.id,
                    "title": c.title,
                    "status": c.status,
                    "severity": c.severity,
                    "message": c.message,
                    "current_value": c.current_value,
                    "suggested_value": c.suggested_value,
                }
                for c in self.checks
            ],
        }

    def __str__(self) -> str:
        """
        Return a human-readable representation of the report.
        """
        lines = []

        summary = self.summary

        if self.passed:
            if summary.warnings > 0:
                result = f"PASS ({summary.warnings} warning(s))"
            else:
                result = "PASS"
        else:
            result = "FAIL"

        lines.append(f"Accessibility Audit ({self.level})")
        lines.append("-" * 40)
        lines.append(f"Score: {self.score}/100")
        lines.append(f"Result: {result}")
        lines.append("")

        for c in self.checks:
            icon = "✓" if c.status == "pass" else "✗"
            lines.append(f"{icon} {c.title}: {c.message}")

        return "\n".join(lines)


def _srgb_channel(value: NumberType) -> float:
    """
    Convert an sRGB channel value into linear space.

    :param value: Channel value in range [0, 1]
    :return: Linearized channel value
    """
    if value <= 0.03928:
        return value / 12.92
    return ((value + 0.055) / 1.055) ** 2.4


def relative_luminance(color: ColorType) -> float:
    """
    Compute the WCAG relative luminance of a color.

    RGBA colors are supported, but alpha values are ignored.

    :param color: RGB or RGBA color
    :return: Relative luminance
    """
    r, g, b = color[:3]

    r = _srgb_channel(r / 255)
    g = _srgb_channel(g / 255)
    b = _srgb_channel(b / 255)

    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(first: ColorType, second: ColorType) -> float:
    """
    Compute the WCAG contrast ratio between two colors.

    :param first: First color
    :param second: Second color
    :return: Contrast ratio
    """
    l1 = relative_luminance(first)
    l2 = relative_luminance(second)

    lighter = max(l1, l2)
    darker = min(l1, l2)

    return (lighter + 0.05) / (darker + 0.05)


def _background_for_widgets(theme: Theme) -> ColorType:
    """
    Return the effective widget background color.

    If the widget background uses a ``BaseImage``, a
    representative color is extracted from the image.

    :param theme: Theme object
    :return: Widget background color
    """
    bg = getattr(theme, "widget_background_color", None)

    if bg is None:
        return theme.background_color

    if isinstance(bg, BaseImage):
        return bg.get_representative_color()

    return bg


def _required_ratio(font_size: int, level: str) -> float:
    """
    Return the minimum contrast ratio required by the
    selected WCAG level.

    :param font_size: Font size
    :param level: WCAG conformance level
    :return: Required contrast ratio
    """
    # Simplified WCAG interpretation used by pygame-menu.
    # Text >= 24px is considered large text.
    large_text = font_size >= 24

    if level.upper() == "AAA":
        return 4.5 if large_text else 7.0

    return 3.0 if large_text else 4.5


def _score(checks: list[AccessibilityCheck]) -> int:
    """
    Compute the accessibility score from audit checks.

    :param checks: Audit checks
    :return: Accessibility score
    """
    score = 100

    for c in checks:
        if c.status != "fail":
            continue

        if c.severity == "error":
            score -= 25
        elif c.severity == "warning":
            score -= 10
        else:
            score -= 2

    return max(score, 0)


def audit_theme(theme: Theme, level: str = "AA") -> AccessibilityReport:
    """
    Audit a theme against WCAG-inspired accessibility rules.

    The audit provides a heuristic accessibility assessment and is
    not a substitute for a full WCAG compliance review.

    The audit evaluates contrast ratios for title text,
    widget text, selection indicators, focus indicators,
    readonly states and scrollbars.

    Supported WCAG levels are ``AA`` and ``AAA``.

    :param theme: Theme to audit
    :param level: WCAG conformance level
    :return: Accessibility audit report
    """
    level = level.upper()

    if level not in ("AA", "AAA"):
        raise ValueError('level must be either "AA" or "AAA"')

    checks: list[AccessibilityCheck] = []

    title_ratio = contrast_ratio(
        theme.title_font_color,
        theme.title_background_color,
    )

    required = _required_ratio(
        theme.title_font_size,
        level,
    )

    checks.append(
        AccessibilityCheck(
            id="title_contrast",
            title="Title contrast",
            status="pass" if title_ratio >= required else "fail",
            severity="error",
            message=(f"{title_ratio:.2f}:1 (required {required:.1f}:1)"),
            current_value=title_ratio,
            suggested_value=required,
        )
    )

    widget_bg = _background_for_widgets(theme)

    widget_ratio = contrast_ratio(
        theme.widget_font_color,
        widget_bg,
    )

    required = _required_ratio(
        theme.widget_font_size,
        level,
    )

    checks.append(
        AccessibilityCheck(
            id="widget_contrast",
            title="Widget contrast",
            status="pass" if widget_ratio >= required else "fail",
            severity="error",
            message=(f"{widget_ratio:.2f}:1 (required {required:.1f}:1)"),
            current_value=widget_ratio,
            suggested_value=required,
        )
    )

    selection_ratio = contrast_ratio(
        theme.selection_color,
        theme.background_color,
    )

    checks.append(
        AccessibilityCheck(
            id="selection_visibility",
            title="Selection visibility",
            status="pass" if selection_ratio >= 3.0 else "fail",
            severity="warning",
            message=f"{selection_ratio:.2f}:1",
            current_value=selection_ratio,
            suggested_value=">= 3.0",
        )
    )

    focus_ratio = contrast_ratio(
        theme.focus_background_color,
        theme.background_color,
    )

    checks.append(
        AccessibilityCheck(
            id="focus_visibility",
            title="Focus visibility",
            status="pass" if focus_ratio >= 3.0 else "fail",
            severity="warning",
            message=f"{focus_ratio:.2f}:1",
            current_value=focus_ratio,
            suggested_value=">= 3.0",
        )
    )

    readonly_ratio = contrast_ratio(
        theme.readonly_color,
        widget_bg,
    )

    checks.append(
        AccessibilityCheck(
            id="readonly_visibility",
            title="Readonly visibility",
            status="pass" if readonly_ratio >= 1.5 else "fail",
            severity="warning",
            message=f"{readonly_ratio:.2f}:1",
            current_value=readonly_ratio,
            suggested_value=">= 1.5",
        )
    )

    scrollbar_ratio = contrast_ratio(
        theme.scrollbar_slider_color,
        theme.scrollbar_color,
    )

    checks.append(
        AccessibilityCheck(
            id="scrollbar_visibility",
            title="Scrollbar visibility",
            status="pass" if scrollbar_ratio >= 3.0 else "fail",
            severity="warning",
            message=f"{scrollbar_ratio:.2f}:1",
            current_value=scrollbar_ratio,
            suggested_value=">= 3.0",
        )
    )

    score = _score(checks)

    passed = not any(c.status == "fail" and c.severity == "error" for c in checks)

    return AccessibilityReport(
        level=level,
        score=score,
        passed=passed,
        checks=checks,
    )
