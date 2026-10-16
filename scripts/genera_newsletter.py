#!/usr/bin/env python3
"""
Genera l'HTML di una newsletter webinar (stessa grafica delle newsletter MailerLite Ideandum).

Uso:
    python3 scripts/genera_newsletter.py data/newsletter/<slug>-1.json

Il JSON contiene:
    oggetto        oggetto della mail
    preheader      testo di anteprima
    titolo_mail    frase sottolineata in apertura (di solito uguale all'oggetto)
    etichetta      es. "MINI CORSO GRATUITO" (predefinito)
    data           AAAA-MM-GG
    ora            HH:MM
    link_landing   https://formazione.ideandum.com/<slug>/
    testo          paragrafi separati da riga vuota; **grassetto**, _corsivo_;
                   l'ultima riga "👉 Iscriviti qui" diventa un link alla landing

Scrive l'HTML accanto al JSON (stesso nome, estensione .html) e lo stampa su stdout se --stdout.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "_template" / "newsletter.html"
MESI = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio",
        "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

SOCIAL = [
    ("linkedin", "https://www.linkedin.com/company/ideandum-s-r-l-/"),
    ("instagram", "https://www.instagram.com/ideandum_"),
    ("facebook", "https://www.facebook.com/ideandum.marketingstudiodentistico"),
    ("whatsapp", "https://wa.me/3402952082"),
    ("youtube", "https://www.youtube.com/channel/UCcsvh8eVQ8e12p4S9nkuHGg"),
]
P = ('<p style="font-family:\'Inter\',sans-serif; color:#000000; font-size:16px; '
     'line-height:165%; margin:0 0 16px;">{}</p>')


def social() -> str:
    celle = "".join(
        f'<td align="center" valign="middle" width="18" style="padding:0 5px;">'
        f'<a href="{u}" target="_blank" style="text-decoration:none;">'
        f'<img src="https://assets.mlcdn.com/ml/images/icons/default/rounded_corners/black/{n}.png" '
        f'width="18" alt="{n}"></a></td>'
        for n, u in SOCIAL
    )
    return ('<table class="mobile-mx-auto" role="presentation" cellpadding="0" '
            f'cellspacing="0" border="0"><tr>{celle}</tr></table>')


def inline(t: str, link: str) -> str:
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"<em>\1</em>", t)
    t = re.sub(r"👉\s*(Iscriviti[^<\n]*)",
               lambda m: f'👉 <a href="{link}" target="_blank" style="color:#e42a80; '
                         f'font-weight:bold; text-decoration:underline;">{m.group(1).strip()}</a>', t)
    return t.replace("\n", "<br>")


def genera(d: dict) -> str:
    for c in ("oggetto", "preheader", "data", "ora", "link_landing", "testo"):
        if not d.get(c):
            sys.exit(f"Campo mancante: {c}")
    link = d["link_landing"]
    if not link.startswith("https://formazione.ideandum.com/"):
        sys.exit("link_landing deve essere una pagina di formazione.ideandum.com")
    a, m, g = (int(x) for x in d["data"].split("-"))
    h, mi = d["ora"].split(":")
    ora = f"{int(h)}:{mi}"
    paragrafi = [p.strip() for p in re.split(r"\n\s*\n", d["testo"]) if p.strip()]
    valori = {
        "OGGETTO": html.escape(d["oggetto"]),
        "PREHEADER": html.escape(d["preheader"]),
        "TITOLO_MAIL": html.escape(d.get("titolo_mail") or d["oggetto"]),
        "ETICHETTA": html.escape(d.get("etichetta") or "MINI CORSO GRATUITO"),
        "DATA_ESTESA": f"{g} {MESI[m - 1]}",
        "ORA": ora,
        "LINK_LANDING": html.escape(link),
        "TESTO": "\n".join("        " + P.format(inline(p, link)) for p in paragrafi),
        "SOCIAL": social(),
    }
    out = TEMPLATE.read_text(encoding="utf-8")
    for k, v in valori.items():
        out = out.replace("{{" + k + "}}", v)
    rimasti = re.findall(r"\{\{\w+\}\}", out)
    if rimasti:
        sys.exit(f"Segnaposto non sostituiti: {rimasti}")
    return out


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    src = Path(args[0])
    out = genera(json.loads(src.read_text(encoding="utf-8")))
    dest = src.with_suffix(".html")
    dest.write_text(out, encoding="utf-8")
    if "--stdout" in sys.argv:
        print(out)
    else:
        print(f"Newsletter generata: {dest}")
