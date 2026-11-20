#!/usr/bin/env python3
"""Rebuild footer page JSON from the JD Hardware pages export."""

from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).with_name("build-pages.py")))
