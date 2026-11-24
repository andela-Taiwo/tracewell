"""Keep personal details out of logs and partial displays.

Tracewell handles health data about named people. Phone numbers, email addresses and health
service numbers must never reach logs or error reports, and lists show only as much of a
person's details as the viewer needs. Redaction is applied by a logging filter so that a
careless log line elsewhere cannot leak them.
"""

from __future__ import annotations

import logging
import re

_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# Health service numbers: 10 digits, often written 3-3-4.
_HEALTH_NUMBER = re.compile(r"(?<!\d)\d{3}[ -]?\d{3}[ -]?\d{4}(?!\d)")
# Phone numbers: optional +, then 9 to 15 digits with spaces, dashes or brackets between.
_PHONE = re.compile(r"(?<![\w+])\+?\(?\d(?:[\d ()-]{7,20})\d(?!\d)")


def redact_text(text: str) -> str:
    """Replace emails, health service numbers and phone numbers in free text."""
    text = _EMAIL.sub("[email]", text)
    text = _HEALTH_NUMBER.sub("[health-number]", text)

    def phone(match: re.Match[str]) -> str:
        digits = sum(ch.isdigit() for ch in match.group(0))
        return "[phone]" if 9 <= digits <= 15 else match.group(0)

    return _PHONE.sub(phone, text)


def mask_phone(phone: str) -> str:
    """Show only the last three digits, e.g. ``*******123``."""
    digits = [ch for ch in phone if ch.isdigit()]
    if len(digits) < 9:
        raise ValueError("not a phone number")
    return "*" * (len(digits) - 3) + "".join(digits[-3:])


def mask_name(name: str) -> str:
    """Show initials only, e.g. ``J. D.``."""
    parts = name.split()
    if not parts:
        raise ValueError("name is empty")
    return " ".join(f"{p[0].upper()}." for p in parts)


def mask_email(email: str) -> str:
    """Show the first character of the mailbox and the domain, e.g. ``j***@example.org``."""
    if _EMAIL.fullmatch(email) is None:
        raise ValueError("not an email address")
    local, domain = email.split("@", 1)
    return f"{local[0]}***@{domain}"


class RedactingFilter(logging.Filter):
    """A logging filter that redacts the formatted message of every record."""

    def filter(self, record: logging.LogRecord) -> bool:
        message = redact_text(record.getMessage())
        record.msg = message
        record.args = None
        if record.exc_info and record.exc_info[1] is not None:
            # Format the traceback now, redacted, so handlers never see the raw one.
            record.exc_text = redact_text(logging.Formatter().formatException(record.exc_info))
            record.exc_info = None
        return True
