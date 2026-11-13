"""Generate local infrastructure credentials without overwriting an existing .env."""

import os
import secrets
from pathlib import Path

root = Path(__file__).resolve().parents[1]
destination = root / ".env"
try:
    descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
except FileExistsError:
    print(".env already exists; left unchanged.")
else:
    template = (root / ".env.example").read_text()
    with os.fdopen(descriptor, "w") as output:
        output.write(template.replace("REPLACE_WITH_GENERATED_PASSWORD", secrets.token_hex(24)))
    print("Created .env with a random local database password. Do not commit it.")
