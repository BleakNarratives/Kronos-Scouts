#!/usr/bin/env python3
"""
scout_runner.py — Integrated Harness
Connects AxeScouts, Agentic Almanac strategic schemas, and SQLite RAG.
"""

import os
import sys
import json
import sqlite3
import time

sys.path.insert(0, os.path.abspath("."))

# Dynamic Adapter Imports
try:
    from adapters import axe_scout_spec
    HAS_AXE = True
except ImportError:
    HAS_AXE = False

# Almanac Module Checks
HAS_ALMANAC = os.path.exists("schema/agent_entry_schema.json")
DB_PATH = "scout_rag_store.db"

def init_rag_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS scraped_knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            domain TEXT,
            title TEXT,
            content TEXT,
            scraped_at REAL
        )
    """)
    cur.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts 
        USING fts5(url UNINDEXED, title, content);
    """)
    conn.commit()
    conn.close()

def load_signals():
    # Scan for fixtures in root or core_framework path
    paths = ["fixtures/market_signals.json", "core_framework/fixtures/market_signals.json"]
    for p in paths:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f), p
    return [], None

def run_harness():
    init_rag_db()
    print("=== Scout Harness Active ===")
    
    if HAS_AXE:
        print("[+] AxeScout specification loaded successfully.")
    else:
        print("[!] AxeScout specification missing.")

    if HAS_ALMANAC:
        print("[+] Agentic Almanac strategic schema verified.")
    else:
        print("[!] Agentic Almanac schema missing.")

    signals, source_path = load_signals()
    if signals:
        print(f"[+] Loaded {len(signals)} dynamic signal targets from: {source_path}")
    else:
        print("[*] Ready for live signal inputs (no market_signals.json fixture found).")

if __name__ == "__main__":
    run_harness()
