"""Build and test real services in an isolated Compose project, then remove only test data."""

import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
command = ["docker", "compose", "-p", "traceleaf-test", "-f", "infra/compose/test.yaml"]
try:
    subprocess.run([*command, "run", "--build", "--rm", "checks"], cwd=root, check=True)
finally:
    subprocess.run([*command, "down", "--volumes", "--remove-orphans"], cwd=root, check=True)
