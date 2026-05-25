#!/usr/bin/env python3
from pathlib import Path
import zipfile

script_path = Path(__file__).resolve().parent

with zipfile.ZipFile(script_path / "layer_commander.zip", "w", zipfile.ZIP_DEFLATED) as zf:
    desktop = script_path / "layer_commander.desktop"
    zf.write(desktop, desktop.name)

    for f in (script_path / "layer_commander").rglob("*"):
        if "__pycache__" in f.parts:
            continue
        zf.write(f, str(f.relative_to(script_path)))
