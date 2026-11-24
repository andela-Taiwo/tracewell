from datetime import date, timedelta

import pytest
from hypothesis import given
from hypothesis import strategies as st

from tracewell.exposure import TracingRules, Window, assess_contact, infectious_window

TEST = date(2026, 3, 10)


def test_symptomatic_case_is_anchored_on_onset() -> None:
    window = infectious_window(TEST, onset=date(2026, 3, 8))
    assert window == Window(date(2026, 3, 6), date(2026, 3, 18))


def test_case_without_symptoms_is_anchored_on_the_test() -> None:
    assert infectious_window(TEST) == Window(date(2026, 3, 8), date(2026, 3, 20))


def test_custom_rules_are_used() -> None:
    rules = TracingRules(days_before_onset=3, days_after_onset=7)
    window = infectious_window(TEST, onset=date(2026, 3, 8), rules=rules)
    assert window == Window(date(2026, 3, 5), date(2026, 3, 15))


def test_windows_cross_month_and_year_ends() -> None:
    assert infectious_window(date(2026, 1, 1)).first == date(2025, 12, 30)
    assert infectious_window(date(2028, 2, 25)).last == date(2028, 3, 6)  # leap year


def test_onset_long_after_the_test_is_rejected() -> None:
    with pytest.raises(ValueError, match="onset"):
        infectious_window(TEST, onset=TEST + timedelta(days=11))


def test_contact_inside_the_window_gets_quarantine_from_last_exposure() -> None:
    window = infectious_window(TEST, onset=date(2026, 3, 8))
    exposure = assess_contact([date(2026, 3, 7), date(2026, 3, 9), date(2026, 3, 7)], window)
    assert exposure is not None
    assert exposure.exposure_dates == (date(2026, 3, 7), date(2026, 3, 9))
    assert exposure.quarantine_until == date(2026, 3, 19)


def test_meetings_outside_the_window_do_not_make_a_contact() -> None:
    window = infectious_window(TEST, onset=date(2026, 3, 8))
    assert assess_contact([date(2026, 3, 5), date(2026, 3, 19)], window) is None
    assert assess_contact([], window) is None


def test_window_edges_are_inclusive() -> None:
    window = infectious_window(TEST, onset=date(2026, 3, 8))
    assert assess_contact([window.first], window) is not None
    assert assess_contact([window.last], window) is not None


@given(
    st.dates(date(2020, 1, 1), date(2030, 12, 31)),
    st.integers(-10, 10),
    st.lists(st.dates(date(2019, 12, 1), date(2031, 1, 31)), max_size=8),
)
def test_quarantine_never_ends_before_the_last_exposure(
    test_date: date, onset_offset: int, meetings: list[date]
) -> None:
    window = infectious_window(test_date, onset=test_date + timedelta(days=onset_offset))
    exposure = assess_contact(meetings, window)
    if exposure is None:
        assert not any(d in window for d in meetings)
    else:
        assert all(d in window for d in exposure.exposure_dates)
        assert exposure.quarantine_until >= exposure.exposure_dates[-1]


@pytest.mark.parametrize("bad", [-1, 61])
def test_rules_out_of_range_are_rejected(bad: int) -> None:
    with pytest.raises(ValueError, match="quarantine_days"):
        TracingRules(quarantine_days=bad)


def test_window_cannot_run_backwards() -> None:
    with pytest.raises(ValueError):
        Window(date(2026, 3, 2), date(2026, 3, 1))
