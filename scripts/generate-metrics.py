#!/usr/bin/env python3
"""Generate a sample .well-known/integrity/metrics.json from protocol/protocol.json"""
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
protocol_path = root / 'protocol' / 'protocol.json'
output_dir = root / '.well-known' / 'integrity'
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / 'metrics.json'

with protocol_path.open() as f:
    proto = json.load(f)

fields = proto.get('integrity_protocol', {}).get('disclosure_schema', {}).get('fields', [])
metrics = {}
for fld in fields:
    if fld == 'model_version':
        metrics[fld] = proto.get('integrity_protocol', {}).get('version', '0.0.0')
    elif fld == 'odds':
        metrics[fld] = proto.get('integrity_protocol', {}).get('operational_spec', {}).get('odds', '')
    elif fld == 'intervention_rate_last_30_days':
        metrics[fld] = 2.3
    elif fld == 'median_time_to_fix':
        metrics[fld] = 45
    elif fld == 'open_audit_cases':
        metrics[fld] = 0
    else:
        metrics[fld] = None

with output_path.open('w') as f:
    json.dump(metrics, f, indent=2)

print(f"Wrote sample metrics to {output_path}")
