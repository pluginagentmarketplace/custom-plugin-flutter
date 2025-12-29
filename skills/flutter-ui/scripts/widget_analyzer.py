#!/usr/bin/env python3
"""Flutter widget analyzer."""
import json
def analyze(): return {"categories": ["stateless", "stateful", "inherited", "render"], "layouts": ["flex", "stack", "custom"]}
if __name__ == "__main__": print(json.dumps(analyze(), indent=2))
