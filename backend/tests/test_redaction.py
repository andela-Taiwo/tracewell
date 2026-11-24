import logging

import pytest

from tracewell.redaction import RedactingFilter, mask_email, mask_name, mask_phone, redact_text

# All personal details below are made up. 07700 900xxx is a range reserved for drama use.


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("call 07700 900123 today", "call [phone] today"),
        ("mobile +44 7700 900123.", "mobile [phone]."),
        ("tel (020) 7946 0958", "tel [phone]"),
        ("email ada.lovelace@example.org now", "email [email] now"),
        ("number 943 476 5919 on file", "number [health-number] on file"),
        ("number 9434765919 on file", "number [health-number] on file"),
    ],
)
def test_redact_text(text: str, expected: str) -> None:
    assert redact_text(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "case 42 has 3 contacts",
        "onset 2026-03-08, test 2026-03-10",
        "postcode SW1A 1AA",
        "ward 12, bed 4",
    ],
)
def test_ordinary_text_is_left_alone(text: str) -> None:
    assert redact_text(text) == text


def test_masks() -> None:
    assert mask_phone("07700 900123") == "********123"
    assert mask_name("ada  king lovelace") == "A. K. L."
    assert mask_email("ada.lovelace@example.org") == "a***@example.org"


@pytest.mark.parametrize(
    "call",
    [lambda: mask_phone("12345"), lambda: mask_name("  "), lambda: mask_email("ada@")],
)
def test_masks_reject_bad_input(call: object) -> None:
    with pytest.raises(ValueError):
        call()  # type: ignore[operator]


def _logger(stream_records: list[str]) -> logging.Logger:
    logger = logging.getLogger("tracewell.test")
    logger.handlers.clear()
    logger.propagate = False

    class Collect(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            stream_records.append(self.format(record))

    handler = Collect()
    handler.addFilter(RedactingFilter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def test_filter_redacts_arguments_as_well_as_the_message() -> None:
    lines: list[str] = []
    _logger(lines).info("called %s at %s", "ada@example.org", "07700 900123")
    assert lines == ["called [email] at [phone]"]


def test_filter_redacts_tracebacks() -> None:
    lines: list[str] = []
    logger = _logger(lines)
    try:
        raise ValueError("bad phone 07700 900123")
    except ValueError:
        logger.exception("import failed")
    assert "900123" not in lines[0]
    assert "[phone]" in lines[0]
