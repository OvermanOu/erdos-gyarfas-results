#!/usr/bin/env python3
"""Top-level verification runner for OvermanOu/erdos-gyarfas-results.

Runs all standalone standard-library verifiers (Paper I and Paper II),
checks JSON certificate parity, asserts status == "PASS", and exits 0.

Usage:
    python verify_all.py
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
VERIFIERS = [
    ("Paper I (Nilpotent Cubic Haar Graphs)", ROOT / "paper1_nilpotent_haar" / "verify_paper1.py"),
    ("Paper II (Sharp 38-Vertex Cubic Bipartite Bound)", ROOT / "paper2_cubic_bipartite_c4c8" / "verify_paper2.py"),
]


def main() -> int:
    results = {}
    for label, script_path in VERIFIERS:
        if not script_path.exists():
            raise FileNotFoundError(f"Missing verifier script: {script_path}")
        proc = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(script_path.parent),
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            sys.stderr.write(f"[FAIL] {label} exited with code {proc.returncode}\n")
            if proc.stdout:
                sys.stderr.write(proc.stdout + "\n")
            if proc.stderr:
                sys.stderr.write(proc.stderr + "\n")
            return proc.returncode or 1

        payload = json.loads(proc.stdout)
        if payload.get("status") != "PASS":
            sys.stderr.write(f"[FAIL] {label} reported status={payload.get('status')!r}\n")
            return 1
        results[label] = payload

    summary = {
        "overall_status": "PASS",
        "verifiers": results,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
