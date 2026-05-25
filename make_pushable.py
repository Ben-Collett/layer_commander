#!/usr/bin/env python3
from pathlib import Path
import shutil

script_path = Path(__file__).resolve()

parent_dir = script_path.parent
grandparent_dir = script_path.parent.parent

src_dir = grandparent_dir / "layer_commander"
dst_dir = parent_dir / "layer_commander"
if dst_dir.exists():
    shutil.rmtree(dst_dir)
shutil.copytree(src_dir, dst_dir)

src_file = grandparent_dir / "layer_commander.desktop"
dst_file = parent_dir / "layer_commander.desktop"
shutil.copy2(src_file, dst_file)
