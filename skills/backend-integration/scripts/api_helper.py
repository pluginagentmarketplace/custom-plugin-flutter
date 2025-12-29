#!/usr/bin/env python3
"""Backend API helper."""
import json
def helper(): return {"http": ["dio", "retrofit"], "auth": ["jwt", "oauth2", "firebase"]}
if __name__ == "__main__": print(json.dumps(helper(), indent=2))
