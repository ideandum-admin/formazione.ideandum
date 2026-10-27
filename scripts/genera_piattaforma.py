#!/usr/bin/env python3
"""
Genera piattaforma/index.html da _template/piattaforma.html e data/piattaforma-video.json.

Uso:
    python3 scripts/genera_piattaforma.py
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def js(s):
    """Stringa sicura dentro un attributo onclick tra apici singoli."""
    return html.escape(s.replace("\\", "\\\\").replace("'", "\\'"), quote=True)


def card(v):
    e = html.escape
    vid = e(v["youtube_id"])
    return (
        f'      <div class="card" data-cat="{e(v["categoria"])}" data-id="{vid}" data-title="{e(v["titolo"])}">\n'
        f'        <div class="card-thumb"><div class="thumb-bg" style="background-image:url(\'https://img.youtube.com/vi/{vid}/hqdefault.jpg\');"></div><div class="thumb-overlay"></div><div class="play-btn"><div class="play-arr"></div></div></div>\n'
        f'        <div class="card-body">\n'
        f'          <div class="card-cat-label">{e(v["etichetta"])}</div>\n'
        f'          <div class="card-title">{e(v["titolo"])}</div>\n'
        f'          <div class="card-desc">{e(v["descrizione"])}</div>\n'
        f'          <button class="watch-btn" onclick="openVid(event,\'{js(v["youtube_id"])}\',\'{js(v["categoria"])}\',\'{js(v["titolo"])}\')">▶ Guarda ora</button>\n'
        f'        </div>\n'
        f'      </div>\n'
    )


def main():
    video = json.loads((ROOT / "data" / "piattaforma-video.json").read_text(encoding="utf-8"))["video"]
    tpl = (ROOT / "_template" / "piattaforma.html").read_text(encoding="utf-8")
    n = len(video)
    out = tpl.replace("{{CARDS}}", "\n".join(card(v) for v in video)).replace(
        "{{CONTEGGIO}}", f"{n} {'contenuto disponibile' if n == 1 else 'contenuti disponibili'}")
    dest = ROOT / "piattaforma" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out, encoding="utf-8")
    print(f"Scritto {dest.relative_to(ROOT)} con {n} video")


if __name__ == "__main__":
    main()
