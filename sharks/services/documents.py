from __future__ import annotations

import re
from typing import Any


def parse_document_text(raw_text: str | None) -> dict[str, Any]:
    if not raw_text:
        return {"message": "OCR is optional and will be enabled later.", "fields": {}}

    patterns = {
        "name": r"Name[:\s]+([A-Za-z ]{3,})",
        "pan": r"[A-Z]{5}[0-9]{4}[A-Z]",
        "income": r"(?:Income|Salary)[:\s₹]*([0-9,]+)",
        "dob": r"(?:DOB|Date of Birth)[:\s]+([0-9/\-]{8,10})",
    }
    fields: dict[str, str] = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, raw_text, flags=re.IGNORECASE)
        if match:
            fields[key] = match.group(1).strip()
    return {"message": "Document parsed in demo mode.", "fields": fields}
