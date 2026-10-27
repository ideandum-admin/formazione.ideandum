#!/usr/bin/env python3
"""
Genera eventi-passati/index.html da _template/eventi-passati.html e data/eventi-passati.json.

Uso:
    python3 scripts/genera_eventi_passati.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    dati = json.loads((ROOT / "data" / "eventi-passati.json").read_text(encoding="utf-8"))
    eventi = sorted(dati["eventi"], key=lambda e: e.get("data_iso", ""), reverse=True)
    lista = [{"titolo": e["titolo"], "sottotitolo": e.get("sottotitolo", ""), "data": e["data"]} for e in eventi]
    # json.dumps produce stringhe JS valide (virgolette e apostrofi gestiti)
    js = json.dumps(lista, ensure_ascii=False, indent=2).replace("</", "<\\/")
    tpl = (ROOT / "_template" / "eventi-passati.html").read_text(encoding="utf-8")
    out = tpl.replace("{{EVENTI}}", js)
    dest = ROOT / "eventi-passati" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out, encoding="utf-8")
    print(f"Scritto {dest.relative_to(ROOT)} con {len(lista)} eventi")


if __name__ == "__main__":
    main()
