from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import re

# ---- Heurísticas simples (opcional) ----
PARTS_OF_DAY = {"morning","afternoon","evening","night","midnight","noon"}

def guess_timex_type(text: str) -> str:
    t = text.strip().lower()
    if re.search(r"\b\d{1,2}:\d{2}(:\d{2})?\b", t):
        return "TIME"
    if any(p in t for p in PARTS_OF_DAY):
        return "TIME"
    if re.search(r"\b\d+\s+(day|days|hour|hours|minute|minutes|week|weeks|month|months|year|years)\b", t):
        return "DURATION"
    return "DATE"

def parse_ns_args(ns_list: List[str]) -> Dict[str, str]:
    """Recebe ['tei=http://...','x=...'] e devolve {'tei':'http://...','x':'...'}."""
    nsmap: Dict[str, str] = {}
    for item in ns_list or []:
        if "=" not in item:
            raise ValueError(f"--ns deve ser prefix=URI (recebido: {item})")
        k, v = item.split("=", 1)
        nsmap[k.strip()] = v.strip()
    return nsmap

# ---- Padrões extras para cobrir casos comuns (EntityRuler) ----
def entity_ruler_patterns() -> List[dict]:
    ordinals = [
        "first","second","third","fourth","fifth","sixth","seventh",
        "eighth","ninth","tenth","eleventh","twelfth",
    ]
    return [
        # HH:MM[:SS]
        {"label": "TIMEX", "pattern": [{"TEXT": {"REGEX": r"^[0-2]?\d:\d{2}(?::\d{2})?$"}}]},
        # the third day / on the third day
        {"label": "TIMEX", "pattern": [{"LOWER": "the"}, {"LOWER": {"IN": ordinals}}, {"LOWER": "day"}]},
        {"label": "TIMEX", "pattern": [{"LOWER": "on"}, {"LOWER": "the"}, {"LOWER": {"IN": ordinals}}, {"LOWER": "day"}]},
        # in the morning/evening/...
        {"label": "TIMEX", "pattern": [{"LOWER": "in"}, {"LOWER": "the"}, {"LOWER": {"IN": list(PARTS_OF_DAY)}}]},
        # durations simples: three days / 3 days
        {"label": "TIMEX", "pattern": [{"LOWER": {"IN": ["one","two","three","four","five","six","seven","eight","nine","ten"]}}, {"LOWER": {"IN": ["day","days","hour","hours","minute","minutes"]}}]},
        {"label": "TIMEX", "pattern": [{"IS_DIGIT": True}, {"LOWER": {"IN": ["day","days","hour","hours","minute","minutes","week","weeks"]}}]},
    ]
