"""Async SMTP delivery of a document to a Kindle address."""
from __future__ import annotations

import mimetypes
import ssl
from email.message import EmailMessage

import aiosmtplib

from config import settings


async def send_to_kindle(
    to_email: str,
    file_path: str,
    filename: str,
    convert: bool = False,
) -> None:
    """Email `file_path` as an attachment to the user's Kindle address.

    Subject "Convert" asks Amazon to convert formats like .docx to Kindle format.
    Raises RuntimeError if SMTP isn't configured, or aiosmtplib errors on send.
    """
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        raise RuntimeError(
            "SMTP is not configured — set SMTP_USER and SMTP_PASSWORD in .env."
        )

    msg = EmailMessage()
    msg["From"] = settings.SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = "Convert" if convert else filename
    msg.set_content("Sent via Kindle Sender Bot.")

    ctype, encoding = mimetypes.guess_type(filename)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)

    # A ≤20 MB read here is unavoidable to build the MIME message; the file was
    # streamed to disk on download and is deleted by the caller right after.
    with open(file_path, "rb") as fh:
        data = fh.read()
    msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=filename)

    tls_context = ssl.create_default_context()
    if not settings.SMTP_VERIFY_HOSTNAME:
        # Tolerate a hostname mismatch (e.g. shared-hosting mail.* alias) while
        # still requiring a CA-valid certificate — connection stays encrypted.
        tls_context.check_hostname = False

    implicit_tls = settings.SMTP_PORT == 465
    await aiosmtplib.send(
        msg,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASSWORD,
        use_tls=implicit_tls,        # implicit TLS on 465
        start_tls=not implicit_tls,  # STARTTLS on 587
        tls_context=tls_context,
    )
