#!/usr/bin/env python3
"""Run M1-M3 separately; restore the original booking module even on failure."""
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
module = root / "app/src/booking.ts"
original = module.read_text()
mutants = [
    ("M1", "end - start > 120", "end - start >= 120"),
    ("M2", "start < booking.end && end > booking.start",
     "start <= booking.end && end >= booking.start"),
    ("M3", "  if (blocked) return false;\n", ""),
]

try:
    for mutant_id, old, new in mutants:
        if old not in original:
            raise SystemExit(f"{mutant_id}: expected source pattern not found; source left unchanged")
        mutated = original.replace(old, new, 1)
        module.write_text(mutated)
        print(f"\n===== {mutant_id} =====", flush=True)
        result = subprocess.run(["npx", "vitest", "run"], cwd=root / "app")
        print(f"{mutant_id}: " + ("SURVIVED" if result.returncode == 0 else "DETECTED"), flush=True)
        module.write_text(original)
finally:
    module.write_text(original)
print("\nOriginal booking.ts restored.")
