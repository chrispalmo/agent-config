#!/usr/bin/env python3
"""Reuse the previous native subscription runner; do not overwrite its evidence."""
import argparse
import importlib.util
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('native_pilot', ROOT.parent / '2026-10-23-skill-pilot/run_pilot.py')
pilot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilot)
pilot.ROOT = ROOT
pilot.REPO = ROOT.parents[3]
pilot.CURSOR_WORKSPACE = Path('/private/tmp/agent-skill-integration-20261023-workspace')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--harness', choices=['claude', 'cursor'], required=True)
    parser.add_argument('--skill', choices=['search-agent-chats', 'triage', 'browser-session'], required=True)
    parser.add_argument('--attempt', type=int, default=1)
    args = parser.parse_args()
    pilot.run(args.harness, args.skill, 'integrated', args.attempt)
