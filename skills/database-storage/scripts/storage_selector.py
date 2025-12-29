#!/usr/bin/env python3
"""Storage solution selector."""
import json
def select(): return {"local": ["shared_prefs", "hive", "sqflite"], "cloud": ["firestore", "supabase"]}
if __name__ == "__main__": print(json.dumps(select(), indent=2))
