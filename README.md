# formazione.ideandum.com

Sito statico delle landing webinar di Ideandum.

## Struttura

```
_assets/            font, immagini, css e tracking.js condivisi (online)
_template/          modello della landing con segnaposto {{...}} (non online)
data/webinar/       una scheda JSON per ogni webinar (non online)
data/esempi/        schede di esempio (non online)
scripts/            generatore delle landing (non online)
<slug>/index.html   landing generate (online su formazione.ideandum.com/<slug>/)
.github/workflows/  pubblicazione automatica via FTP a ogni push su main
```

## Nuovo webinar

1. Creare `data/webinar/<slug>.json` (vedi `data/esempi/pazienti-web.json`).
2. `python3 scripts/genera_landing.py data/webinar/<slug>.json`
3. Commit e push su `main` → la pagina va online su `formazione.ideandum.com/<slug>/`.

Nei testi della scheda si può usare `**grassetto**`.

Ogni landing invia al webhook Zapier, oltre ai dati del form, `event_id` e `consenso_newsletter`.

**Webhook unico** per tutti i nuovi webinar: `https://hooks.zapier.com/hooks/catch/2042357/41itfwa/` (Zap "Webinar – Zap unico").
Lo Zap cerca `event_id` nel foglio **WEBINAR AUTOMAZIONE** del file "2026 - BDU" e ne prende titolo, data, ora, link Zoom e gruppo MailerLite.

Istruzioni per il primo setup: vedi `ISTRUZIONI-WEBMASTER.md`.
