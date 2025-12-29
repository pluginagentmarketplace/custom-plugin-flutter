#!/usr/bin/env python3
"""Flutter deployment helper."""
import json
def deploy(): return {"ci": ["github_actions", "codemagic"], "stores": ["play_store", "app_store"]}
if __name__ == "__main__": print(json.dumps(deploy(), indent=2))
