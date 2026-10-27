#!/usr/bin/env python3
"""
Genera eventi-sito/prossimi-webinar.js a partire da data/eventi-sito.json.

Il file JS viene letto dal widget HTML di Elementor nella sezione
"Prossimi Eventi Gratuiti" di ideandum.com/marketing-odontoiatria/#eventi
(codice del widget: eventi-sito/widget-elementor.html).

Uso:
    python3 scripts/genera_eventi_sito.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SORGENTE = ROOT / "data" / "eventi-sito.json"
DEST = ROOT / "eventi-sito" / "prossimi-webinar.js"
BASE = "https://formazione.ideandum.com"

# Parametri UTM dei click dal carosello eventi del sito ideandum.com
# (stessa logica delle linee guida: source = da dove, medium = canale,
#  campaign = formato, content = formato + descrizione).
UTM = ("utm_source=sito-ideandum&utm_medium=sito"
       "&utm_campaign=carosello&utm_content=carosello-prossimi-eventi")


def main():
    dati = json.loads(SORGENTE.read_text(encoding="utf-8"))
    eventi = []
    for e in dati["eventi"]:
        for campo in ("slug", "titolo", "data", "immagine"):
            if not e.get(campo):
                sys.exit(f"Evento senza '{campo}': {e}")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", e["data"]):
            sys.exit(f"Data non valida (AAAA-MM-GG): {e['data']}")
        img = e["immagine"]
        if img.startswith("/"):
            if not (ROOT / img.lstrip("/")).exists():
                sys.exit(f"Immagine mancante nel repository: {img}")
            img = BASE + img
        eventi.append({
            "titolo": e["titolo"],
            "data": e["data"],
            "ora": e.get("ora", ""),
            "immagine": img,
            "link": f"{BASE}/{e['slug']}/?{UTM}",
        })
    eventi.sort(key=lambda x: x["data"])
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(
        "/* Generato da scripts/genera_eventi_sito.py: non modificare a mano */\n"
        "window.IDEANDUM_PROSSIMI_WEBINAR = "
        + json.dumps(eventi, ensure_ascii=False, indent=2)
        + ";\n"
        "if (window.IDEANDUM_PROSSIMI_WEBINAR_PRONTO) window.IDEANDUM_PROSSIMI_WEBINAR_PRONTO();\n",
        encoding="utf-8",
    )
    print(f"Scritto {DEST.relative_to(ROOT)} con {len(eventi)} eventi")

    # Pagina di anteprima del widget (stesso codice da incollare in Elementor)
    widget = (ROOT / "eventi-sito" / "widget-elementor.html").read_text(encoding="utf-8")
    anteprima = (
        "<!doctype html>\n<html lang=\"it\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        "<meta name=\"robots\" content=\"noindex\"><title>Anteprima carosello eventi</title>"
        "<style>body{margin:0;background:#e9e9e9;font-family:Inter,Arial,sans-serif;padding:40px 16px}"
        "h2{text-align:center;font-size:44px;line-height:1;margin:0 0 30px}</style></head><body>"
        "<h2>Prossimi<br>Eventi Gratuiti</h2>\n" + widget + "\n</body></html>\n"
    )
    (ROOT / "eventi-sito" / "anteprima.html").write_text(anteprima, encoding="utf-8")
    print("Scritto eventi-sito/anteprima.html")


if __name__ == "__main__":
    main()
