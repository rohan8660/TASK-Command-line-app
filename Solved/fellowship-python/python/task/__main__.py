"""Task entry point script."""
# task/__main__.py

from task import (    ERRORS, __app_name__, __version__,  config,   database,   task, cli )
from pathlib import Path
from typing import List, Optional
import typer

def main():
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()