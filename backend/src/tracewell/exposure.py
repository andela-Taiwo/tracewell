"""Infectious periods, exposure windows and isolation and quarantine dates.

A contact tracer's first question about a case is "from when to when could they have
infected someone?". Everyone the case met in that window is a contact, and each contact's
quarantine runs from their last exposure. Getting a date wrong by one day sends someone back
to work too early, so the rules are explicit, configurable and tested.

The default numbers are examples only. A health authority sets the real ones for each
disease; Tracewell stores them per outbreak and never treats them as medical advice.
All dates are calendar dates; day counts are inclusive of the start date's day 0.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class TracingRules:
    days_before_onset: int = 2
    """Days before symptoms start that a case counts as infectious."""
    days_after_onset: int = 10
    days_before_test: int = 2
    """For a case with no symptoms: days before the positive test."""
    days_after_test: int = 10
    quarantine_days: int = 10
    """Days a contact stays in quarantine after their last exposure."""

    def __post_init__(self) -> None:
        for name, value in vars(self).items():
            if not isinstance(value, int) or not 0 <= value <= 60:
                raise ValueError(f"{name} must be a whole number of days from 0 to 60")


@dataclass(frozen=True)
class Window:
    """An inclusive range of calendar dates."""

    first: date
    last: date

    def __post_init__(self) -> None:
        if self.last < self.first:
            raise ValueError("a window cannot end before it starts")

    def __contains__(self, day: object) -> bool:
        return isinstance(day, date) and self.first <= day <= self.last


def infectious_window(
    test_date: date, onset: date | None = None, rules: TracingRules | None = None
) -> Window:
    """Return the dates a case counts as infectious.

    With symptoms the window is anchored on onset; without, on the positive test date.
    """
    r = rules or TracingRules()
    if onset is not None:
        if onset > test_date + timedelta(days=r.days_after_onset):
            raise ValueError("symptom onset is too long after the test to belong to this case")
        return Window(
            onset - timedelta(days=r.days_before_onset), onset + timedelta(days=r.days_after_onset)
        )
    return Window(
        test_date - timedelta(days=r.days_before_test),
        test_date + timedelta(days=r.days_after_test),
    )


@dataclass(frozen=True)
class Exposure:
    exposure_dates: tuple[date, ...]
    """Meetings that fell inside the case's infectious window, earliest first."""
    quarantine_until: date
    """Last day of quarantine (inclusive)."""


def assess_contact(
    met_on: Iterable[date], window: Window, rules: TracingRules | None = None
) -> Exposure | None:
    """Return the exposure for someone who met the case on ``met_on``, or None if no meeting
    fell inside the infectious window (they are not a contact)."""
    r = rules or TracingRules()
    inside = tuple(sorted({d for d in met_on if d in window}))
    if not inside:
        return None
    return Exposure(inside, inside[-1] + timedelta(days=r.quarantine_days))
