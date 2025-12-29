#!/usr/bin/env python3
"""Flutter test generator helper."""
import json
def generate(): return {"types": ["unit", "widget", "integration", "golden"], "coverage_target": 80}
if __name__ == "__main__": print(json.dumps(generate(), indent=2))
