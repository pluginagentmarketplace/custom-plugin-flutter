#!/usr/bin/env python3
"""State management selector."""
import json
def select(): return {"simple": ["setState", "ValueNotifier"], "medium": ["Provider", "Riverpod"], "complex": ["BLoC", "Redux"]}
if __name__ == "__main__": print(json.dumps(select(), indent=2))
