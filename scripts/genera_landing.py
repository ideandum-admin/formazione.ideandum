#!/usr/bin/env python3
"""
Genera una landing webinar a partire da una scheda JSON.

Uso:
    python3 scripts/genera_landing.py data/webinar/<slug>.json

Crea (o sovrascrive) la cartella <slug>/index.html nella radice del repository,
partendo da _template/index.html. Nel testo delle schede si può usare **grassetto**.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "_template" / "index.html"

CAMPI_OBBLIGATORI = [
    "slug", "event_id", "titolo", "sottotitolo", "data_breve", "ora",
    "relatori", "testo", "argomenti", "motivi", "webhook_url",
]


def testo(t: str) -> str:
    """Escape HTML e converte **grassetto** in <b>."""
    t = html.escape(t, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)


def relatori(lista):
    out = []
    for r in lista:
        out.append(
            '        <div class="speaker">\n'
            f'          <img src="{html.escape(r["foto"])}" alt="{html.escape(r["nome"])}">\n'
            f'          <span class="speaker-name">{html.escape(r["nome"])}</span>\n'
            "        </div>"
        )
    return "\n".join(out)


def paragrafi(lista):
    return "\n".join(f"        <p>{testo(p)}</p>" for p in lista)


def argomenti(lista):
    out = []
    for a in lista:
        out.append(
            '        <div class="icon-box">\n'
            '          <i class="fas fa-check icon-box-icon"></i>\n'
            "          <div>\n"
            f'            <div class="icon-box-title">{testo(a["titolo"])}</div>\n'
            f'            <div class="icon-box-desc">{testo(a["descrizione"])}</div>\n'
            "          </div>\n"
            "        </div>"
        )
    return "\n".join(out)


def motivi(lista):
    return "\n".join(f'      <div class="nope-item">{testo(m)}</div>' for m in lista)


def genera(scheda_path: Path) -> Path:
    d = json.loads(scheda_path.read_text(encoding="utf-8"))
    mancanti = [c for c in CAMPI_OBBLIGATORI if not d.get(c)]
    if mancanti:
        sys.exit(f"Campi mancanti nella scheda: {', '.join(mancanti)}")
    if not re.fullmatch(r"[a-z0-9-]+", d["slug"]):
        sys.exit("Lo slug può contenere solo lettere minuscole, numeri e trattini.")
    if not d["webhook_url"].startswith("https://hooks.zapier.com/"):
        sys.exit("webhook_url non valido: deve essere un URL hooks.zapier.com")

    valori = {
        "TITOLO_PAGINA": html.escape(d.get("titolo_pagina") or d["titolo"]),
        "META_DESCRIPTION": html.escape(d.get("meta_description") or d["sottotitolo"][:155]),
        "DATA_BREVE": html.escape(d["data_breve"]),
        "ORA": html.escape(d["ora"]),
        "TITOLO": testo(d["titolo"]),
        "SOTTOTITOLO": testo(d["sottotitolo"]),
        "RELATORI": relatori(d["relatori"]),
        "TESTO": paragrafi(d["testo"]),
        "ARGOMENTI": argomenti(d["argomenti"]),
        "MOTIVI": motivi(d["motivi"]),
        # valori dentro stringhe JavaScript: niente apici
        "WEBHOOK_URL": d["webhook_url"].replace("'", ""),
        "EVENT_ID": d["event_id"].replace("'", "’"),
    }

    out = TEMPLATE.read_text(encoding="utf-8")
    for k, v in valori.items():
        out = out.replace("{{" + k + "}}", v)
    rimasti = re.findall(r"\{\{\w+\}\}", out)
    if rimasti:
        sys.exit(f"Segnaposto non sostituiti: {rimasti}")

    dest = ROOT / d["slug"] / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out, encoding="utf-8")
    return dest


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(f"Landing generata: {genera(Path(sys.argv[1]))}")
