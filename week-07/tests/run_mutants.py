#!/usr/bin/env python3
"""Run M1-M3 one at a time and always restore the booking implementation."""
from pathlib import Path
import subprocess
root=Path(__file__).resolve().parents[1]
module=root/'app/src/booking.ts'
original=module.read_text()
mutants=[('M1','if (end-start > 120)','if (end-start >= 120)'),('M2','start < booking.end && end > booking.start','start <= booking.end && end >= booking.start'),('M3','  if (blocked) return false;\n','')]
try:
 for mid,old,new in mutants:
  if old not in original: raise SystemExit(f'{mid}: source pattern missing')
  module.write_text(original.replace(old,new,1))
  print(f'--- {mid} ---',flush=True)
  result=subprocess.run(['npx','vitest','run'],cwd=root/'app')
  print(f'{mid}: '+('SURVIVED' if result.returncode==0 else 'DETECTED'),flush=True)
  module.write_text(original)
finally: module.write_text(original)
