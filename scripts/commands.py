#!/usr/bin/env python
# mypy: ignore-errors
import argparse
import os
import subprocess
import sys
from typing import List, Optional


def run_command(cmd: List[str], cwd: Optional[str] = None) -> int:
    """Run a command and stream output in real-time."""
    print(f"Running: {' '.join(cmd)}")
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=cwd
    )

    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            print(output.strip())

    return process.poll()


def setup_venv() -> None:
    """Set up the virtual environment."""
    run_command(["uv", "venv"])
    run_command(["uv", "pip", "install", "--upgrade", "pip"])
    run_command(["uv", "pip", "install", "-e", "."])
    print("\033[32mDevelopment environment ready!\033[0m")


def lint() -> int:
    """Run mypy type checking."""
    return run_command(["uv", "run", "mypy", "."])


def format_code() -> int:
    """Format code with ruff."""
    status1 = run_command(["uv", "run", "ruff", "--exit-non-zero-on-fix", "--fix-only"])
    status2 = run_command(["uv", "run", "ruff", "format"])
    status3 = run_command(["uv", "run", "ruff", "format", "--check"])
    return max(status1, status2, status3)


def sync_dependencies() -> int:
    """Sync dependencies from lock file."""
    return run_command(["uv", "pip", "sync", "requirements.lock"])


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Autheon development command runner")
    parser.add_argument(
        "command",
        choices=[
            "setup",
            "lint",
            "format",
            "sync",
        ],
        help="Command to run",
    )

    args = parser.parse_args()

    commands = {
        "setup": setup_venv,
        "lint": lint,
        "format": format_code,
        "sync": sync_dependencies,
        "info": lambda: print(f"Running on {os.uname().machine} machine"),
    }

    exit_code = commands[args.command]()
    sys.exit(exit_code if isinstance(exit_code, int) else 0)

if __name__ == "__main__":
    main()
