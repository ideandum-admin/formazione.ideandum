# Procedura webinar Ideandum – riferimento tecnico

Riferimento operativo per le skill prepara-, avvia- e chiudi-webinar-ideandum: ID, strumenti, passi dettagliati. Le regole di contenuto e tono sono in `docs/linee-guida-contenuti.md`. Come le linee guida, questo documento prevale sulle skill: le modifiche si fanno qui, su richiesta di Luigi.

Indice: 1. Avvio (campi della scheda, valori fissi, UTM, modello HTML, mail agli iscritti, passi, dopo l'ok grafiche, revisione, modifiche) · 2. Chiusura (valori fissi, post webinar, report)

# 1. Avvio

### Campi della scheda

Pagina schede: https://claude.ai/artifact/Mw1vvQAiTEiKDPw2Ct3K5q — database, collezione `webinar`, documento = slug (minuscole, numeri e trattini).

- Landing: `titolo`, `sottotitolo`, `data` (AAAA-MM-GG), `ora` (HH:MM, di solito 13:00), `slug`, `event_name_extended`, `event_id` (`Webinar - AAAA.MM.GG - <Event Name Extended>`), `relatori` [{`nome`, `foto`}], `testo` (paragrafi separati da riga vuota, `**grassetto**` ammesso), `argomenti` [4 x {`titolo`, `descrizione`}], `motivi` [3 stringhe], facoltativi `logo` e `logo_alt`.
- Gestione: `note`, `stato` (`bozza` | `pronta` | `avviata` | `chiusa`), `aggiornato` (ISO), `approvati` {`landing`, `annunci`, `newsletter`, `whatsapp`}.
- `nome_breve` (1-2 parole per i nomi degli annunci).
- `annunci`: {`titolo_annuncio` (es. "Webinar gratuito · 1 Dicembre ore 13"), `descrizione` ("Online · Gratuito · Posti limitati"), `angoli`: [3 x {`lettera`, `grafica_titolo`, `grafica_sottotitolo`, `testo_freddo`, `testo_caldo`}]}. Il testo è uno solo per angolo: salvalo identico nei due campi.
- `newsletter`: [2 x {`oggetto`, `oggetto_b` (obbligatorio nella 1, vuoto nella 2), `preheader`, `testo` (senza "Ciao,", firma e P.S.; il link si scrive `[puoi iscriverti qui]`), `ps`, `firma`, `mittente`, `titolo_mail` (vuoto, non si usa più)}].
- `whatsapp` (testo del messaggio).
- Dopo l'avvio: `landing_url`, `webinar_link`, `zoom_meeting_id`, `mailerlite_group`, `canva_link`, `youtube_cover_link`, `youtube_cover_design_id`, `meta` (ID gruppo e annunci), `avviato_il`. Dopo la chiusura: `youtube_id`, `youtube_url`, `chiuso_il`.
- **Foto relatori per la landing**: i file sono in `_assets/img/` del repository (es. Armida `/_assets/img/Armida-Parigi.webp`, Chiara Tessarotto `/_assets/img/chiara-tessarotto.jpg`); controlla lì prima di chiedere. Per un relatore nuovo Luigi carica la foto dalla pagina schede (meglio se scontornata).

### Valori fissi

- Pagina schede: https://claude.ai/artifact/Mw1vvQAiTEiKDPw2Ct3K5q — database, collezione `webinar`, documento = slug (campi descritti nella skill prepara-webinar-ideandum e qui sotto in "Campi della scheda"; campi facoltativi `logo` e `logo_alt` = logo mostrato sopra il titolo della landing; `youtube_cover_link` e `youtube_cover_design_id` = copertina YouTube)
- Linee guida contenuti: `docs/linee-guida-contenuti.md` nel repository, in particolare "Impostazione annunci per ogni webinar", "Carosello Prossimi Eventi Gratuiti sul sito", "Parametri UTM degli annunci", "Grafiche (Canva)", "Modelli per le creatività" e "Foto dei relatori"
- Repository: `ideandum-admin/formazione.ideandum` (branch `main`; il push pubblica in automatico via FTP su formazione.ideandum.com). Per clone e push serve un token GitHub che Luigi fornisce; non scriverlo mai nel repository. Lo stato della pubblicazione si legge dall'API GitHub (`actions/runs`). La pubblicazione FTP carica i file nuovi ma **non cancella** mai quelli sul server.
- Generatore landing: `python3 scripts/genera_landing.py data/webinar/<slug>.json`
- Generatore carosello eventi del sito: `python3 scripts/genera_eventi_sito.py` (legge `data/eventi-sito.json`, scrive `eventi-sito/prossimi-webinar.js` e `eventi-sito/anteprima.html`)
- Generatore piattaforma: `python3 scripts/genera_piattaforma.py` (legge `data/piattaforma-video.json`, scrive `piattaforma/index.html`; la pagina non contiene chiavi API: non aggiungerne mai)
- Generatore pagina eventi passati: `python3 scripts/genera_eventi_passati.py` (legge `data/eventi-passati.json`)
- Newsletter: **non usare più** `scripts/genera_newsletter.py` né `_template/newsletter.html` (impaginazione promozionale con logo, social, pulsanti e box). Le newsletter si costruiscono con il modello "mail personale" della sezione "Modello HTML newsletter" qui sotto.
- Impostazioni Zoom standard: `scripts/zoom_riunione.json` del repository (registrazione automatica nel cloud, necessaria per il post webinar)
- Zoom (via Zapier, app Zoom, account conference@ideandum.com): `POST https://api.zoom.us/v2/users/me/meetings`; lettura e modifica con `GET`/`PATCH https://api.zoom.us/v2/meetings/<id>`. La risposta contiene `registration_url` (link di iscrizione) e `join_url` (link per accedere alla riunione); mai usare `start_url`.
- MailerLite (via Zapier): connessione "MailerLite Ideandum (Greta Portinari)" `connection_id` 02b64f68-a471-8b23-97f1-0ddd796a48ee — passala sempre esplicitamente; mai usare la connessione predefinita (è Amantide, un altro cliente)
- Azioni MailerLite personalizzate (Zapier, code action; nessuna invia o programma mai):
  - `code_action_mailerlitev2cliapi__mailerlite_crea_bozza_campagna`: mode `create` crea una bozza normale (`name`, `subject`, `from_name`, `from_email`, `content`, `group_ids`); mode `delete_draft` elimina una campagna solo se è in bozza (`campaign_id`, vale anche per le A/B).
  - `code_action_mailerlitev2cliapi__mailerlite_crea_bozza_ab_oggetto`: crea una bozza **A/B split sull'oggetto** (`name`, `subject_a`, `subject_b`, `from_name`, `from_email`, `content`, `group_ids`, `test_split` in %, `winner_by` = `o` aperture / `c` click, `after_hours`).
  - `code_action_mailerlitev2cliapi__mailerlite_info_account`: sola lettura (`groups`, `segments`, `campaigns` con `status`, `campaign` con `campaign_id`).
  - Se una creazione restituisce un errore temporaneo (es. Service Unavailable), prima di riprovare controlla con `campaigns` / status `draft` che la bozza non sia già stata creata, per evitare doppioni.
- Tabella webinar (via Zapier, Google Sheets, account automation@ideandum.com): file "2026 - BDU" `1wS-OmWkP47ztSJmg0hj45JQfC23Pt68LNqLA9W0C0c8`, foglio WEBINAR AUTOMAZIONE `434054097`. Colonne: A event_id, B event_name_extended, C event_date (GG/MM/AAAA), D event_time (HH:MM), E webinar_link (registration_url, letto dallo Zap e da IDEHUB/AISA), F mailerlite_group (ID numerico del gruppo), G slug, H zoom_meeting_id, I stato, J note, K canva_link (link al design Canva "– ADS" con le creatività), L zoom_join_link (join_url per accedere alla riunione), M landing_url, N data_estesa (giorno e data per esteso, minuscolo: es. `martedì 10 novembre`), O titolo_mail (titolo della landing fino ai due punti, senza punto finale: es. `Più pazienti di implantologia nel tuo studio nel 2027`). N e O servono alla mail di conferma (vedi "Mail agli iscritti")
- Webhook unico (già impostato dal generatore): https://hooks.zapier.com/hooks/catch/2042357/41itfwa/ — Zap "Webinar – Zap unico", che legge la tabella con l'event_id
- Canva (connettore Canva):
  - **Modelli delle creatività**: design "Template Campagne Ideandum" `DAHYLLZt2rA` (preparato da Luigi; non modificarlo mai). Modelli: **Aura** = pagine 1 (quadrato) + 2 (storia); **Chiaro** = 3 + 4; **Rosa** = 5 + 6; **Live** = 8 (quadrato; la 7 è 4:5 e non si usa; finché non c'è una storia Live, usa Live solo se Luigi aggiunge la pagina storia). Nel modello Aura i riquadri bianchi dietro le parole chiave sono forme separate da riposizionare.
  - **Copertina YouTube** (1280×720): dall'11/11/2026 è l'**ultima pagina del design "– ADS"** del webinar. Si parte dalla copertina del webinar precedente (ultima pagina del suo design "– ADS"; per i webinar fino al 24/11/2026 era un design a parte "– YouTube", es. `DAHZN2FONXc`), aggiunta in fondo con merge-designs (insert_pages). Stile: sfondo sfumato viola/blu con onde, testo grande bianco = titolo della landing, riga sotto in nero = nome breve o tema del webinar.
  - **Archivio foto relatori**: design "Foto team - risorse umane" `DAF_TrHtOgY`, foto divise per persona con i nomi aggiunti da Luigi. Registro delle foto usate: `docs/archivio-relatori.md` nel repository. L'archivio ha 499 pagine e **non si può aprire in transazione**: per ricavare il `mediaId` di una foto, copia le sole pagine che servono con copy-design in un design di lavoro, leggilo lì con open_transaction e chiudi con `cancel`. Se la foto ha ancora lo sfondo, scontornala con remove-background.
  - Kit del brand "Ideandum". La generazione automatica di design di Canva non si usa (provata e scartata).
  - Le modifiche di testo con find_and_replace_text/replace_text **uniscono le regioni di formattazione** dell'elemento (grassetto/colori misti diventano uniformi): controlla l'anteprima e, se serve, riformatta o segnala a Luigi il ritocco manuale. Un testo aggiunto con add_text non usa il font del brand: non usarlo per i titoli.
- **Scaricare file nel workspace** (export Canva, immagini di siti esterni): il workspace non raggiunge export-download.canva.com né i siti esterni. Carica il file su Drive con Zapier (Google Drive "Upload File" da URL, account digital@ideandum.com), condividilo con il dominio ideandum.com ("Add File Sharing Preference", org_link_view) e scaricalo con il connettore Google Drive `download_file_content`; per file grandi il risultato viene salvato su disco come JSON con `content` in base64. Controlla l'md5 rispetto a quello restituito da Drive. Non ricopiare mai a mano il base64.
- YouTube (via Zapier): connessione del canale **Ideandum** @ideandums.r.l.4863 `connection_id` 02871620-35d0-8d1d-8a33-6c0a3e319386 (predefinita); non usare la connessione "YouTube" del canale Digital Ideandum.
- Meta Ads: account Ideandum Srl `113096912423590`, campagna CBO "Webinar - 2026 - Budget per webinar (CBO)" `52600961859122` con **un gruppo per ogni webinar** ("Webinar AAAA.MM.GG – <nome_breve>") e il gruppo "Webinar – Nuovo pubblico" `52602074974122`; struttura e spese minime nelle linee guida contenuti (sezione "Struttura della campagna e budget"). Pagina Facebook `1413838048854984`, Instagram `17841400100973320`.
- **Parametri UTM** (sezione "Parametri UTM degli annunci" delle linee guida, aggiornata l'11/11/2026): ogni creatività porta `url_tags` = `utm_source={{site_source_name}}&utm_medium=<pubblico>&utm_campaign=<slug>&utm_content=<formato>-<descrizione>&utm_term={{placement}}`. `utm_medium` = `remarketing` nei gruppi per webinar, `freddo` nel gruppo "Webinar – Nuovo pubblico". `utm_campaign` = slug del webinar. `utm_content` = formato + descrizione breve in minuscolo con trattini (es. `immagine-angolo-a`, `video-franco-pensieroso`). Il link resta la landing pulita: i parametri vanno solo in `url_tags`, mai nel link. Lo stesso contenuto in due gruppi cambia solo `utm_medium`.
- Le bozze create tramite API (Meta MCP) **non compaiono in Gestione inserzioni**: per renderle visibili a Luigi vanno pubblicate, sempre in pausa (vedi "Dopo l'ok grafiche").

### UTM su tutti i link (obbligatorio)

Ogni link alla landing che esce da Ideandum porta i parametri UTM: senza UTM il report di fine webinar (skill chiudi-webinar-ideandum) non può dire quale canale ha portato iscritti e partecipanti. È successo con "Abbattere il Carico Fiscale": nessun dato per canale. Usa sempre `utm_campaign` = slug del webinar, minuscole e trattini.

| Canale | Parametri da aggiungere al link della landing |
|---|---|
| Annunci Meta | in `url_tags`, mai nel link (vedi "Parametri UTM" nei Valori fissi) |
| Newsletter 1 (entrambe le versioni A/B) | `?utm_source=newsletter&utm_medium=email&utm_campaign=<slug>&utm_content=newsletter-1` |
| Newsletter 2 | `?utm_source=newsletter&utm_medium=email&utm_campaign=<slug>&utm_content=newsletter-2` |
| WhatsApp (community) | `?utm_source=whatsapp&utm_medium=community&utm_campaign=<slug>` |
| Post social organici (link in bio, storie, post) | `?utm_source=instagram` (o `facebook`, `linkedin`) `&utm_medium=organico&utm_campaign=<slug>&utm_content=<tipo>-<descrizione>` |
| Partner o relatori esterni | `?utm_source=<nome-partner>&utm_medium=partner&utm_campaign=<slug>` |
| Carosello eventi del sito | già aggiunti dallo script |

- I promemoria agli iscritti puntano al link Zoom: lì niente UTM.
- Mai un link "nudo" alla landing in newsletter, messaggi, post o materiali per i partner.
- **IDEHUB**: la landing invia l'URL completo nel campo `pagina` e lo Zap unico deve salvarlo nella colonna Note di RAW_CONTACTS; è lì che il report legge il canale. Se la colonna Note delle iscrizioni del webinar è vuota, le UTM non servono a nulla: avvisa subito Luigi (va controllata la mappatura del campo `pagina` nello Zap unico; questa skill non modifica gli Zap).

### Modello HTML newsletter (mail personale)

Le newsletter devono sembrare una mail scritta a mano: sfondo bianco, testo semplice allineato a sinistra, nessun logo, nessuna immagine, nessuna icona social, nessun pulsante, nessun box colorato, nessuna emoji. Un solo link nel testo (la landing) più il link obbligatorio per annullare l'iscrizione. Sostituisci i segnaposto `{{...}}`:

- `{{OGGETTO}}` = `oggetto` (per la Newsletter 1 l'oggetto A); `{{PREHEADER}}` = `preheader`
- `{{PARAGRAFI}}` = il `testo` diviso sulle righe vuote, ogni paragrafo in `<p style="margin:0 0 16px;">…</p>` (anche la riga in grassetto "WEBINAR · …" è un paragrafo a sé); `**x**` → `<strong>x</strong>`; `[testo]` → `<a href="<landing_url con le UTM della newsletter, vedi 'UTM su tutti i link'>" style="color:#1a0dab;text-decoration:underline;">testo</a>`
- `{{FIRMA}}` = `firma` (di solito "Armida")
- `{{PS}}` = `ps` (la riga "P.S. …"); se `ps` è vuoto, togli l'intero paragrafo del P.S. e riporta a 32px il margine sotto la firma
- `{$unsubscribe}` è il segnaposto di MailerLite: lascialo così

```html
<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{OGGETTO}}</title>
</head>
<body style="margin:0;padding:0;background:#ffffff;">
<span style="display:none;font-size:1px;line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;">{{PREHEADER}}</span>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#ffffff;">
<tr>
<td style="padding:24px 16px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:560px;">
<tr>
<td style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.6;color:#222222;">
<p style="margin:0 0 16px;">Ciao,</p>
{{PARAGRAFI}}
<p style="margin:0 0 4px;">A presto,</p>
<p style="margin:0 0 24px;">{{FIRMA}}</p>
<p style="margin:0 0 32px;">{{PS}}</p>
<p style="margin:0;font-size:12px;line-height:1.5;color:#888888;">Ideandum · Via Vecchia Ferriera 5, Vicenza<br>Ricevi questa email perché ti sei iscritto sul nostro sito o hai partecipato a un nostro evento. <a href="{$unsubscribe}" style="color:#888888;text-decoration:underline;">Annulla l'iscrizione</a></p>
</td>
</tr>
</table>
</td>
</tr>
</table>
</body>
</html>
```

Se il `testo` salvato nella scheda inizia già con "Ciao," o finisce con la firma o il P.S., non duplicarli.

### Mail agli iscritti (conferma e promemoria)

Tutti gli iscritti dalla landing entrano nel gruppo MailerLite del webinar (il consenso nel modulo è obbligatorio). Sequenza approvata da Luigi il 3/11/2026, testi fissi da non riscrivere:

| Mail | Quando | Come |
|---|---|---|
| Conferma | subito dopo l'iscrizione | automazione MailerLite unica (campi `webinar_titolo`, `webinar_data`, `webinar_ora`, `webinar_link` scritti dallo Zap dalle colonne O, N, D, E) — non si tocca a ogni webinar |
| Promemoria 2 giorni prima | 2 giorni prima, ore 9:00 | bozza di campagna al gruppo del webinar (passo 9) |
| Promemoria giorno prima | giorno prima, ore 9:00 | bozza di campagna al gruppo del webinar |
| Avviso giorno stesso | giorno del webinar, ore 11:00 (con webinar alle 13; altrimenti 2 ore prima) | bozza di campagna al gruppo del webinar |

Promemoria: modello HTML della newsletter, firma "Armida", senza P.S. (margine 32px sotto la firma), saluto finale indicato sotto al posto di "A presto,". `<link>` = `webinar_link` (colonna E, uguale per tutti), testo del link "entra nel webinar". `<titolo>` = titolo_mail; `<data>` = data_estesa; `<ora>` = ora senza minuti se tonda (es. `13`); `<relatori>` = "con me e X" se Armida è relatrice (es. "con me e Franco Valerio"), altrimenti "con X e Y"; `<Giorno>` = giorno della settimana con iniziale maiuscola; `<argomento>` = breve complemento sul tema (es. "sull'implantologia", "sulle riunioni di team").

1. **Promemoria 2 giorni prima** — oggetto `<Giorno> alle <ora> ci sei?`; preheader `Il webinar <argomento> è tra due giorni.`; paragrafi: `ti ricordo che **<data> alle <ora>** c'è il webinar "<titolo>", <relatori>.` / `Se non l'hai già fatto, bloccati l'ora in agenda adesso: in studio le giornate si riempiono in fretta.` / `Il link per partecipare è questo: [entra nel webinar](<link>).`; saluto `A presto,`.
2. **Promemoria giorno prima** — oggetto `Domani alle <ora>, ci vediamo online`; preheader `Ecco il link per entrare.`; paragrafi: `domani alle <ora> c'è il webinar "<titolo>".` / `Un consiglio pratico: entra 5 minuti prima, così sistemi audio e video con calma. Puoi partecipare anche dal browser, senza installare niente.` / `Il link è questo: [entra nel webinar](<link>).`; saluto `Ci vediamo domani,`.
3. **Avviso giorno stesso** — oggetto `Oggi alle <ora>: ecco il link per entrare`; preheader `Tra due ore iniziamo, ti aspettiamo.`; paragrafi: `oggi alle <ora> iniziamo il webinar "<titolo>".` / `Entra da qui qualche minuto prima: [entra nel webinar](<link>).`; saluto `Ti aspettiamo,`.

I promemoria **non si programmano**: li programma Luigi (per ora; potrà decidere in futuro di affidarli a Claude).

### Passi dell'esecuzione

1. **Scheda**: ArtifactData `get` (collezione `webinar`, doc_id = slug). Prosegui solo se `stato` = `pronta` e `approvati` ha `landing`, `annunci`, `newsletter`, `whatsapp` tutti true; altrimenti di' a Luigi quali testi mancano e torna alla skill prepara-webinar-ideandum. Eccezione: se Luigi chiede esplicitamente di eseguire solo una parte (es. solo le newsletter), basta che sia approvato il blocco di quella parte. Se `event_id` è vuoto usa `Webinar - AAAA.MM.GG - <event_name_extended>` (se il webinar esiste già, prendi l'event_id dal nome del gruppo MailerLite o dalla tabella). Verifica che la data sia futura. Se Luigi ha cambiato lo slug nella scheda (documento rinominato), usa il nuovo.
2. **Repository**: assicurati che il repository sia collegato e clonato; fai pull. Se la cartella `<slug>/` esiste già e non è di questo webinar, fermati e chiedi.
3. **Foto relatori per la landing**: per ogni `foto` che inizia con `asset:` scarica il file con Artifact `read` (url della pagina schede, `path` = l'id dopo `asset:`), salvalo in `_assets/img/<nome-cognome>.<estensione>` e aggiorna la scheda con il nuovo percorso. Se la foto è indicata come pagina dell'archivio Canva, copiala in un design di lavoro, scontornala se serve, esportala in PNG con sfondo trasparente e portala nel workspace con il metodo Drive (vedi "Scaricare file nel workspace"); salvala quadrata 1024×1024 webp, mezzo busto.
4. **Zoom**: se esiste già una riunione per questo webinar (cerca per titolo tra le riunioni in programma) usala: leggi `registration_url`, `join_url` e `id` con GET e allinea `topic`, `start_time` e `settings.auto_recording` = `cloud` se diversi. Altrimenti creala con il body di `scripts/zoom_riunione.json`, `topic` = titolo della landing, `start_time` = `<data>T<ora>:00`, timezone Europe/Rome.
5. **MailerLite**: cerca un gruppo con nome = event_id (elenco completo con `mailerlite_info_account` mode `groups`, perché Find a Group restituisce un solo risultato approssimato); se non esiste crealo (Create Subscribers Group, con la connessione Ideandum). Salva l'ID numerico.
6. **Tabella**: aggiungi la riga in WEBINAR AUTOMAZIONE (o aggiornala, se esiste già una riga con quell'event_id) con event_id, event_name_extended, data GG/MM/AAAA, ora HH:MM, registration_url (E), ID gruppo, slug, ID riunione, stato `attivo`, join_url (L), `https://formazione.ideandum.com/<slug>/` (M), data_estesa (N) e titolo_mail (O). La colonna K si compila al passo 8.
7. **Landing**: scrivi `data/webinar/<slug>.json` copiando i campi della scheda (il generatore accetta il formato della scheda, compresi `logo` e `logo_alt`) e genera la pagina. Controllala con uno screenshot locale, poi commit e push su main. Verifica il workflow "Pubblica sito" (il sito non è raggiungibile dal workspace: chiedi a Luigi di aprirlo).
8. **Grafiche Canva dai modelli** (mai ricrearle fuori da Canva, mai generarle con l'AI di Canva):
   - **Scegli i modelli**: ogni angolo A, B, C usa un modello diverso tra Aura, Chiaro e Rosa (Live solo se ha anche la storia). Guarda nel registro `docs/archivio-relatori.md` l'abbinamento del webinar precedente e cambialo. Il modello Chiaro (sfondo bianco) serve sempre, perché è la grafica usata nel carosello eventi del sito.
   - **Scegli le foto**: per ogni relatore della scheda cerca le sue foto nell'archivio `DAF_TrHtOgY` (sezione con il suo nome; per vedere le foto usa read-design con le miniature delle pagine della sezione). Per Armida Parigi, Franco Valerio e Chiara mai la stessa foto del webinar precedente e, se possibile, foto diverse tra A, B, C; preferisci mezzo busto e sguardo in camera. Per il `mediaId` usa il design di lavoro (vedi Valori fissi). Se un relatore non è nell'archivio, usa la foto della scheda caricandola in Canva (create-upload-url) e, se serve, remove-background; segnalalo nel riepilogo.
   - **Crea la copia**: con copy-design dal design dei modelli crea "Webinar - AAAA.MM.GG - <Nome> - ADS" con le pagine dei modelli scelti, nell'ordine A (quadrato, storia), B, C.
   - **Compila**: con read-design (open_transaction) + edit-design sostituisci in ogni pagina titolo/sottotitolo con `grafica_titolo` e `grafica_sottotitolo` dell'angolo, data, giorno della settimana, ora e nomi dei relatori (dove il modello li ha); sostituisci la foto del relatore con `update_fill` (asset = mediaId scelto). Nel modello Aura sposta e ridimensiona i riquadri bianchi sulle nuove parole chiave del titolo (le parole in nero). Controlla ogni anteprima (testo nei margini, non sovrapposto al relatore o alla data, riquadri allineati alle parole; se serve ridimensiona o sposta) e salva (commit).
   - **Copertina YouTube**: aggiungi in fondo al design "– ADS" la copertina del webinar precedente con merge-designs (insert_pages; prima controlla che non ci sia già una pagina 1280×720, per non duplicarla); sostituisci il testo grande con il titolo della landing e la riga sotto con il nome breve o il tema del webinar (es. "GAIA, la segretaria AI"); bilancia le posizioni dei due testi, controlla l'anteprima e salva. Salva nella scheda `youtube_cover_link` (link di modifica del design "– ADS") e `youtube_cover_design_id` (ID del design "– ADS"). La usa la procedura post webinar come miniatura del video.
   - Annota nel registro `docs/archivio-relatori.md` (commit e push) per questo webinar: modelli usati per A/B/C e foto usate per ogni relatore.
   - Scrivi il link di modifica del design "– ADS" nella colonna K (Update Spreadsheet Row).
   - **Non esportare e non caricare su Meta**: le grafiche aspettano l'ok di Luigi (vedi "Dopo l'ok grafiche").
9. **Newsletter**: per ognuna delle due newsletter della scheda costruisci l'HTML con il "Modello HTML newsletter" (link = landing con le UTM della newsletter: `https://formazione.ideandum.com/<slug>/?utm_source=newsletter&utm_medium=email&utm_campaign=<slug>&utm_content=newsletter-1` per la Newsletter 1, `newsletter-2` per la 2; nello screenshot controlla che il link abbia i parametri), salvalo nella cartella di lavoro e controllalo con uno screenshot locale (testo leggibile, riga WEBINAR in grassetto, P.S. dopo la firma, un solo link nel corpo, nessuna immagine). Poi crea le bozze con la connessione Ideandum, `from_name` = `mittente` della scheda (di solito `Armida Parigi – Ideandum`), `from_email` = `digital@ideandum.com`, `content` = HTML generato, `group_ids` vuoto (tutti gli iscritti attivi). Non passare il preheader all'API: è già nell'HTML.
   - **Newsletter 1: sempre in test A/B sull'oggetto**, con `mailerlite_crea_bozza_ab_oggetto`: `name` = `<event_id> – Newsletter 1 – A/B`, `subject_a` = `oggetto`, `subject_b` = `oggetto_b`, `test_split` = 25, `winner_by` = `o`, `after_hours` = 4. Se nella scheda manca `oggetto_b`, fermati e chiedi a Luigi il secondo oggetto (proponine uno coerente con le regole della skill prepara-webinar-ideandum), poi salvalo nella scheda. Non creare anche una bozza normale della Newsletter 1.
   - **Newsletter 2**: bozza normale con `mailerlite_crea_bozza_campagna` mode `create`, `name` = `<event_id> – Newsletter 2`, `subject` = `oggetto`.
   - **Promemoria agli iscritti**: le 3 bozze della sezione "Mail agli iscritti" con `mailerlite_crea_bozza_campagna` mode `create`, `group_ids` = **ID del gruppo MailerLite del webinar** (mai vuoto: vanno solo agli iscritti), stesso mittente, `name` = `<event_id> – Promemoria 2 giorni prima` / `– Promemoria giorno prima` / `– Avviso giorno stesso`. Controlla prima con uno screenshot che link e data siano giusti.
10. **Pausa annunci, tracciamento e chiusura**: non si programma niente. Li gestiscono le attività programmate giornaliere (linee guida, "Attività programmate"), che leggono la tabella e la scheda: basta che riga in tabella (stato `attivo`) e `avviato_il` siano compilati.
11. **Aggiorna la scheda** (ArtifactData `update` con if_version): `stato` = `avviata`, `landing_url`, `webinar_link`, `zoom_meeting_id`, `mailerlite_group`, `canva_link`, `youtube_cover_link`, `avviato_il` (data e ora); nelle `note` gli ID delle bozze MailerLite (Newsletter 1 A/B, Newsletter 2 e i 3 promemoria).
12. **Riepilogo per la revisione** (un solo messaggio): link landing, link Zoom (iscrizione e accesso), gruppo MailerLite, riga tabella, le 2 newsletter in bozza (la 1 in A/B con i due oggetti, 25% di test, vincitore sulle aperture dopo 4 ore) con le date consigliate (Newsletter 1 subito, Newsletter 2 due giorni prima del webinar), data in cui l'attività programmata metterà in pausa gli annunci (giorno prima alle 12:30), messaggio WhatsApp pronto da copiare **con il link con le UTM di WhatsApp**, i link con le UTM pronti per i post social e per eventuali partner o relatori esterni, il **link del design Canva ADS** con le anteprime delle 6 grafiche e il **link della copertina YouTube**, e la richiesta: "Controlla le grafiche e la copertina YouTube, ritoccale in Canva se vuoi, poi scrivimi *ok grafiche* e creo gli annunci su Meta, pubblicati in pausa". Ricorda a Luigi, in breve, cosa resta a lui in MailerLite:
    - **escludere il gruppo MailerLite del webinar** quando programma (chi è già iscritto non deve ricevere l'invito); per la Newsletter 2 farlo all'ultimo, così il gruppo è aggiornato;
    - impostare la **lingua della campagna in italiano** (le bozze create via API risultano in inglese);
    - **programmare** le due campagne e i **3 promemoria** (indica le date e gli orari esatti: 2 giorni prima ore 9, giorno prima ore 9, giorno stesso ore 11); i promemoria vanno solo al gruppo del webinar, quindi lì il gruppo **non** si esclude;
    - se vuole, fare un test su mail-tester.com prima dell'invio.

### Dopo l'ok grafiche (quando Luigi scrive "ok grafiche" o simile)

1. Rileggi il design "– ADS" senza transaction_id (ultima versione salvata, con i ritocchi di Luigi) e non aprire transazioni di modifica. Le pagine 1-6 sono le grafiche (A, B, C: quadrato e storia), l'ultima è la copertina YouTube. Se il numero o l'ordine delle pagine è diverso, chiedi a Luigi quale pagina corrisponde a quale angolo.
2. Esporta le 6 pagine in PNG (export-design) e caricale su Meta con nome `Webinar AAAA.MM.GG – <nome_breve> – A|B|C quadrato|storia` (ads_creative_upload_media, upload_source URL con il link dell'export). Se Meta non riesce a scaricare un'immagine, riesporta quella pagina e riprova.
3. **Gruppo di inserzioni**: crea nella campagna CBO il gruppo `Webinar AAAA.MM.GG – <nome_breve>` come copia del gruppo del webinar precedente (stessi pubblico, ottimizzazione, evento del pixel e attribuzione; `source_adset_id` = gruppo precedente; leggi le sue impostazioni con ads_get_ad_entities e ripassale: `promoted_object` = pixel 774485682652320, `custom_event_type` OTHER, `custom_event_str` "Webinar"). **Non impostare la spesa minima**: proponi a Luigi i minimi secondo la tabella delle linee guida (se i webinar attivi sono più di tre, proponi come gestirli) e impostali solo dopo il suo ok; se servono cambi futuri (es. dopo la pausa di un webinar), segnalali a Luigi: se diventano ricorrenti, si aggiungono come attività programmata.
4. **Annunci**: un annuncio per angolo (A, B, C), con il testo unico dell'angolo (`testo_freddo`, identico a `testo_caldo`), `titolo_annuncio`, `descrizione`, CTA SIGN_UP, link = landing (senza parametri) e `url_tags` = `utm_source={{site_source_name}}&utm_medium=remarketing&utm_campaign=<slug>&utm_content=immagine-angolo-a|b|c&utm_term={{placement}}` (vedi "Parametri UTM"). Nome: `Webinar AAAA.MM.GG – <nome_breve> – A|B|C`. **Ogni annuncio porta sempre entrambe le grafiche, quadrato e storia**: crealo con `ads_create_ad` e creatività inline con `asset_feed_spec` (non con `ads_create_creative`, che rifiuta la personalizzazione per posizionamento). In `asset_feed_spec`: `images` con i due hash etichettati `quadrato` e `storia` (`adlabels`), `bodies`, `titles`, `descriptions`, `link_urls`, `call_to_action_types` = ["SIGN_UP"], `ad_formats` = ["SINGLE_IMAGE"], `optimization_type` = "PLACEMENT" e `asset_customization_rules`: priorità 1 → `storia` su facebook (`story`, `facebook_reels`) e instagram (`story`, `reels`); priorità 2 → `quadrato` su facebook, instagram e threads. In `object_story_spec` solo `page_id` e `instagram_user_id`; `url_tags` va nella creatività inline, accanto ad `asset_feed_spec`. Non creare annunci con la sola grafica quadrata. Non impostare date di fine sull'annuncio. Niente video, salvo richiesta. **Ogni altro annuncio** creato in seguito (video, post esistenti con `object_story_id`, caroselli, copie nel gruppo Nuovo pubblico) porta sempre `url_tags` con formato e descrizione propri e `utm_medium` del gruppo in cui va. `ads_get_creatives` non restituisce `url_tags`: controlla che siano nello spec restituito da `ads_create_ad` e chiedi a Luigi di verificarli in Gestione inserzioni.
5. **Pubblica in pausa**: con `ads_update_entity` imposta `status` = `PAUSED` sul gruppo e sui 3 annunci in bozza, poi pubblicali con `ads_activate_entity` passando in `object_ids` solo il gruppo e i suoi annunci, con `publish_as_active` = false. Non pubblicare altre bozze della campagna se Luigi non lo chiede. Verifica con `ads_get_ad_entities` (stato live; filtra gli annunci per nome o per gruppo, perché subito dopo la pubblicazione gli ID diretti possono non essere ancora leggibili) che gruppo e annunci risultino PAUSED. **Ripeti la stessa verifica dopo ogni pubblicazione successiva** (per esempio una modifica al pubblico del gruppo): una ripubblicazione può riportare il gruppo ad ACTIVE. Se qualcosa risulta attivo, mettilo subito in pausa e dillo a Luigi.
6. **Carosello eventi del sito** (ideandum.com/marketing-odontoiatria/#eventi): esporta da Canva la grafica quadrata **a sfondo bianco (modello Chiaro)** del webinar (preferisci sempre quella con sfondo bianco), portala nel workspace con il metodo Drive, salvala 800×800 webp in `_assets/img/eventi/<slug>.webp`, aggiungi l'evento in `data/eventi-sito.json` (`slug`, `titolo`, `data`, `ora`, `immagine`), lancia `python3 scripts/genera_eventi_sito.py`, controlla l'anteprima in locale, commit e push. Gli UTM dei link li aggiunge lo script; il giorno dopo il webinar l'evento passa da solo nel carosello "Eventi Passati". Non serve toccare Elementor. Anteprima online: https://formazione.ideandum.com/eventi-sito/anteprima.html
7. Conferma a Luigi in un messaggio breve: gruppo e 3 annunci pubblicati in pausa, webinar aggiunto al carosello del sito, cosa resta da fare (spesa minima, da impostare dopo il suo ok) e che li accende lui quando è pronto.

### Fase 3: revisione di Luigi

- **Ritocchi in Canva dopo che gli annunci sono già su Meta**: quando Luigi scrive di aver modificato il design, rileggilo (read-design senza transaction_id), riesporta le pagine cambiate e sostituisci le immagini negli annunci (annuncio nuovo con lo stesso nome e la nuova creatività, sempre con quadrato e storia e gli stessi `url_tags`, pubblicato in pausa; metti in pausa o elimina il vecchio solo se Luigi lo conferma). Se cambia la grafica Chiaro, aggiorna anche l'immagine del carosello del sito. Non aprire transazioni di modifica mentre Luigi lavora sul design.
- **Correzioni di testo** (landing, annunci, newsletter): applica la correzione alla scheda e rigenera solo ciò che ne dipende (landing → push; annuncio → nuova versione pubblicata in pausa; newsletter in bozza → `delete_draft` + nuova bozza con il modello HTML personale: la Newsletter 1 sempre di nuovo in A/B con `mailerlite_crea_bozza_ab_oggetto`, la 2 normale). Se cambia il titolo della landing, aggiorna anche la copertina YouTube, la colonna O della tabella e i 3 promemoria in bozza. Non attivare annunci e non inviare né programmare newsletter.

### Modifiche dopo la pubblicazione

Quando Luigi chiede di cambiare un webinar già avviato (in chat, oppure dicendo che ha modificato la scheda):

1. Applica la modifica alla scheda (ArtifactData `update` con if_version) o rileggila se l'ha cambiata lui.
2. Aggiorna `data/webinar/<slug>.json`, rigenera la landing, controllala con uno screenshot, commit e push. Verifica il workflow "Pubblica sito".
3. Allinea il resto in base al tipo di modifica:
   - **Solo testi o relatori**: nient'altro, salvo il titolo, che va aggiornato anche nella riunione Zoom (PATCH `topic`), in `data/eventi-sito.json` e nella copertina YouTube.
   - **Data o ora**: aggiorna la riunione Zoom (PATCH `start_time`), le colonne C e D della riga in tabella (Update Spreadsheet Row), la data nel design Canva "– ADS" con nuove immagini negli annunci, l'evento e l'immagine del carosello del sito, (la pausa annunci la gestisce l'attività programmata leggendo la nuova data in tabella). Se le newsletter sono ancora in bozza, rigenerale con la nuova data: elimina le vecchie bozze (`delete_draft`) e creane di nuove (Newsletter 1 in A/B). Aggiorna la colonna N e rigenera allo stesso modo i 3 promemoria; se Luigi li aveva già programmati, avvisalo di annullare la programmazione (una campagna programmata non si elimina con `delete_draft`). L'event_id e il gruppo MailerLite restano invariati. Ricorda a Luigi che gli iscritti già registrati vanno avvisati e offri il testo del messaggio.
   - **Cartella (slug)**: sconsigliala, perché cambia l'indirizzo usato da annunci, newsletter e link già condivisi. Se Luigi conferma, crea la nuova cartella, lascia nella vecchia una pagina di rimando alla nuova, aggiorna le colonne G e M, la scheda (nuovo documento, vecchio eliminato), i link degli annunci, il carosello del sito e le newsletter in bozza.
4. Riepiloga a Luigi cosa è cambiato e dove.

Per tornare a una versione precedente della landing usa la cronologia git del repository (revert del commit e push).

# 2. Chiusura

### Valori fissi

- Pagina schede: https://claude.ai/artifact/Mw1vvQAiTEiKDPw2Ct3K5q — database, collezione `webinar`, documento = slug (campi utili: `event_id`, titolo e sottotitolo della landing, data, ora, relatori, programma, `zoom_meeting_id`, `youtube_cover_design_id`, `youtube_cover_link`).
- Linee guida: `docs/linee-guida-contenuti.md`, sezione "8. YouTube (registrazioni)" (titolo, descrizione, tag, foglio WEBINAR YOUTUBE).
- Repository `ideandum-admin/formazione.ideandum`, branch `main`: il push pubblica via FTP su formazione.ideandum.com e **non cancella** mai file sul server. Generatori: `python3 scripts/genera_piattaforma.py` (`data/piattaforma-video.json`), `python3 scripts/genera_eventi_passati.py` (`data/eventi-passati.json`). Il carosello eventi del sito sposta il webinar negli "Eventi Passati" da solo: non serve toccarlo.
- Zoom (Zapier, app Zoom, account conference@ideandum.com):
  - registrazione: GET `https://api.zoom.us/v2/meetings/<zoom_meeting_id>/recordings` (azione "Make API GET Request") → `uuid`, `duration`, `share_url`, `recording_files` (MP4 `shared_screen_with_speaker_view`, M4A, CHAT). La trascrizione Zoom non è attiva e i link `download_url` non sono scaricabili dal workspace né dalle richieste API.
  - file video: azione "Find Recording and Download" con `meeting_uuid` = `uuid` → restituisce `file`, un link temporaneo all'MP4 che le altre azioni Zapier (YouTube, Drive) accettano come file. Dal workspace non è raggiungibile.
- YouTube (Zapier, connessione del canale **Ideandum** @ideandums.r.l.4863 `connection_id` 02871620-35d0-8d1d-8a33-6c0a3e319386, id canale `UCcsvh8eVQ8e12p4S9nkuHGg`; mai la connessione del canale Digital Ideandum). Azioni: "Upload Video", "Update Video Thumbnail" (PNG o JPG, massimo 2 MB), "Make API GET Request" e "Make API Mutating Request" su `https://www.googleapis.com/youtube/v3/...`.
- Canva: copertina = ultima pagina 1280×720 del design "– ADS" (`youtube_cover_design_id` della scheda); per i webinar fino al 24/11/2026 è un design a parte "– YouTube".
- Foglio "2026 - BDU" `1wS-OmWkP47ztSJmg0hj45JQfC23Pt68LNqLA9W0C0c8`:
  - foglio **WEBINAR YOUTUBE** (sheetId `1405115043`): A FORMAZIONE ESTIVA (lasciare vuota), B MACRO TEMA, C TITOLO, D LINK AL WEBINAR, E DATA WEBINAR (GG/MM/AAAA). I webinar sono in alto; sotto ci sono righe vuote e poi la sezione "INTERVISTE" in colonna B, che non va toccata. Scrivi con il connettore Google Sheets (get_values, insert_dimension, update_values).
  - foglio **WEBINAR AUTOMAZIONE** (via Zapier, Google Sheets automation@ideandum.com, sheet `434054097`): colonna I `stato`, J `note`.
- Scaricare file nel workspace (export Canva, immagini): metodo Drive della sezione 1 (Zapier Drive "Upload File" da URL → condivisione con il dominio ideandum.com → Google Drive `download_file_content`; controlla l'md5).

### A. Post webinar: passi

1. **Dati del webinar**: leggi la scheda (ArtifactData `get`, doc_id = slug) e la riga in WEBINAR AUTOMAZIONE. Verifica che il webinar sia già avvenuto. Se la scheda o la riga non esistono (webinar avviati prima di questa procedura, come Architettura), ricava titolo, data e slug da `data/eventi-sito.json`, l'ID della riunione da Zoom (cerca per titolo tra le registrazioni con GET `https://api.zoom.us/v2/users/me/recordings` con `from`/`to`) e la copertina YouTube cercando in Canva il design del webinar (pagina "YT Thumbnail"); segnala nel riepilogo cosa mancava.
2. **Registrazione Zoom**: GET delle registrazioni della riunione. Se non c'è ancora o qualche file non è `completed`, avvisa Luigi e fermati: l'attività programmata riprova il giorno dopo (oppure Luigi lo chiede prima in chat). Se ci sono più MP4 (diretta interrotta e ripresa), usa il più lungo e segnalalo a Luigi. Annota `uuid`, durata e `share_url`.
3. **Copertina**: esporta la pagina 1280×720 del design indicato da `youtube_cover_design_id` in JPG (export-design; se supera 2 MB riesporta con qualità più bassa). Tieni il link dell'export: Zapier lo accetta come file.
4. **Testi YouTube** (sezione 8 delle linee guida, nessuna approvazione richiesta):
   - **Titolo**: breve, pratico, diretto, ottimista, al massimo 100 caratteri; di solito il titolo della landing, accorciato se serve.
   - **Descrizione**: intro di 2-3 frasi (dal sottotitolo e dal programma della landing, con i relatori) → ⏱️ COSA TROVI IN QUESTO VIDEO (3-5 punti dal programma) → 🦷 A CHI È RIVOLTO → 🔗 RISORSE UTILI (sempre "🌐 Ideandum (marketing per studi dentistici): https://www.ideandum.com", più i siti dei partner citati nella landing, es. GAIA https://ideandumgaia.com) → i capitoli si aggiungono al passo 11 → hashtag di settore (#marketingodontoiatrico #studiodentistico …). Niente link Zoom, niente dati non presenti nella landing.
   - **Tag**: i tag fissi del canale (marketing odontoiatrico, web marketing, marketing, pubblicità, advertising, marketing per dentisti, marketing studi odontoiatrici, apertura studio dentistico, ideanum, consulenza marketing dentista) più 2-4 tag sul tema.
5. **Caricamento su YouTube**: prima controlla che il video non sia già sul canale (GET `search` con `forMine=true`, `type=video`, `q` = titolo). Poi "Find Recording and Download" (`meeting_uuid`) e subito "Upload Video" con `video` = il `file` restituito, `title`, `description`, `tags`, `privacy_status` = `unlisted` (**sempre non in elenco**), `category_id` = `27` (Istruzione), `default_language` e `default_audio_language` = `it`, `made_for_kids` = false, `notify_subscribers` = false, `embeddable` = true, `recording_date` = data del webinar, `thumbnail` = link dell'export JPG, connessione del canale Ideandum. Verifica con GET `videos?part=snippet,status&id=<id>`: `privacyStatus` = `unlisted` e `channelId` = `UCcsvh8eVQ8e12p4S9nkuHGg` (se il video è finito pubblico o su un altro canale, rendilo subito non in elenco e avvisa Luigi). Se la miniatura non risulta impostata, usa "Update Video Thumbnail"; se YouTube la rifiuta per la verifica del telefono, dillo a Luigi.
   - Se il caricamento fallisce per le dimensioni o per un errore che si ripete, non insistere: manda a Luigi lo `share_url` della registrazione Zoom e chiedigli di caricarla a mano come non in elenco con titolo e descrizione che gli prepari; quando ti dà il link, prosegui dal passo 6.
6. **Link a Luigi** subito: `https://youtu.be/<id>`, con il titolo usato. Se la registrazione inizia o finisce con tempi morti, suggerisci il taglio nell'editor di YouTube Studio (non si fa via API).
7. **Piattaforma**: aggiungi il video **in cima** a `data/piattaforma-video.json` con `youtube_id`, `categoria` (uno dei filtri: 'Segreteria & Gestione', 'Marketing', 'Paziente', 'Management', 'Digitale & AI'), `etichetta` (breve, come le altre: Segreteria, Marketing, Brand, AI Marketing, Architettura…), `titolo` con un'emoji iniziale come gli altri video e `descrizione` di 1-2 frasi concrete. Lancia `python3 scripts/genera_piattaforma.py`, controlla la pagina con uno screenshot locale, commit e push. Non aggiungere mai chiavi API alla pagina.
8. **Foglio WEBINAR YOUTUBE**: leggi `'WEBINAR YOUTUBE'!A1:E80`. Se il link del video c'è già, salta il passo. Trova la riga con "INTERVISTE" in colonna B e, sopra di essa, l'ultima riga con un link in colonna D: è l'ultimo webinar (riga N). Inserisci una riga subito sotto con insert_dimension (`sheetId` 1405115043, ROWS, `startIndex` = N, `endIndex` = N+1, `inheritFromBefore` = true) e scrivi `'WEBINAR YOUTUBE'!A<N+1>:E<N+1>` = ["", macro tema, titolo, `https://youtu.be/<id>`, data GG/MM/AAAA]. Il macro tema riprende i valori già usati in colonna B (es. Segreteria efficace, Marketing, Brand, Imprenditorialità del titolare di studio, Soluzione Tasse, Architettura, Intelligenza Artificiale); il titolo è quello del webinar. Rileggi per verificare che la riga sia sopra le righe vuote e la sezione INTERVISTE. Se il connettore non può scrivere, usa Zapier (Google Sheets, automation@ideandum.com) e aggiorna la prima riga vuota sotto l'ultimo webinar, lasciando almeno una riga vuota prima di INTERVISTE; se non ce n'è, chiedi a Luigi di aggiungerne una.
9. **Eventi passati**:
   - Se la cartella `<slug>/` della landing è nel repository, spostala con `git mv <slug> eventi-passati/<slug>` (le immagini usano percorsi assoluti `/_assets/...`, quindi la pagina funziona anche lì). Se non è nel repository (landing caricate a mano sul server, come Architettura), lo spostamento sul server lo fa Luigi: diglielo.
   - Aggiungi l'evento in cima a `data/eventi-passati.json` (`data_iso` AAAA-MM-GG, `data` "4 Novembre 2026", `titolo` e `sottotitolo` della landing, `slug`), lancia `python3 scripts/genera_eventi_passati.py`, controlla con uno screenshot, commit e push.
   - Ricorda a Luigi che la vecchia cartella `/<slug>/` resta sul server (la pubblicazione non cancella): può eliminarla lui quando vuole; finché c'è, i link di annunci e newsletter funzionano.
10. **Tabelle e scheda**: in WEBINAR AUTOMAZIONE metti `stato` = `concluso` e nelle `note` il link YouTube (Update Spreadsheet Row; non toccare le altre colonne). Aggiorna la scheda (ArtifactData `update` con if_version): `stato` = `chiusa`, `youtube_id`, `youtube_url`, `chiuso_il` (data e ora).
11. **Capitoli (seconda parte)**: i sottotitoli automatici di YouTube sono pronti qualche ora dopo il caricamento. Se non sono ancora pronti, i capitoli li aggiunge l'attività programmata del giorno dopo (o Luigi lo chiede in chat). Quando li fai:
    - GET `https://www.googleapis.com/youtube/v3/captions` con `part=snippet` e `videoId`; serve una traccia `trackKind` = `asr`, `language` = `it`, `status` = `serving`. Se non c'è, rimanda al giorno dopo; se manca ancora dopo 2 giorni, chiedi a Luigi il file SRT.
    - Scarica la traccia: GET `https://www.googleapis.com/youtube/v3/captions/<caption_id>` con `tfmt=srt`. Il risultato è lungo e viene salvato su file: leggilo con Python a pezzi e salva l'SRT nella cartella di lavoro come `<slug>-youtube.srt`.
    - Individua 6-12 capitoli in base ai cambi di argomento: il primo a `00:00`, almeno 10 secondi tra uno e l'altro, titoli brevi in italiano (es. "00:00 Introduzione e relatori"), formato `MM:SS` o `H:MM:SS`. Salta i tempi morti iniziali indicandoli come "Inizio" solo se durano più di un minuto.
    - Aggiorna la descrizione: GET `videos?part=snippet&id=<id>`, inserisci la sezione ⏱️ CAPITOLI prima degli hashtag, poi PUT `videos?part=snippet` ("Make API Mutating Request") con l'intero snippet (`title`, `description`, `tags`, `categoryId`, `defaultLanguage`, `defaultAudioLanguage`): la PUT sostituisce tutto lo snippet. Verifica con una GET e scrivi a Luigi in un messaggio breve che i capitoli sono stati aggiunti.
12. **Riepilogo** (un solo messaggio, dopo il passo 10): link YouTube non in elenco, video aggiunto in piattaforma, riga nel foglio WEBINAR YOUTUBE (numero di riga), landing in `/eventi-passati/<slug>/` (o cosa deve spostare Luigi sul server), capitoli (aggiunti o rimandati all'attività del giorno dopo), e cosa è mancato o andrebbe controllato (miniatura, tagli, video pubblico se Luigi lo vuole). Poi passa alla parte B (report).

### B. Report del webinar

Obiettivo: capire quante persone si sono iscritte e hanno partecipato, da quale canale, quante erano nuove per IDEHUB e quanto è costato Meta; aggiornare il foglio di confronto tra webinar; poi un'infografica da girare ai colleghi. Modello approvato da Luigi: infografica "Webinar Marketing e Architettura – Risultati" https://claude.ai/artifact/9M1eiztt7PEDP1ojBuPnxa.

#### Fonti

- **IDEHUB** (Google Sheets "IDEHUB v.1.0", `1xpnRjokmjmaKbv9KK5HjAIOUNpJN-bXaoXORC0yi13c`, solo lettura):
  - `EVENTS` (intestazioni alla riga 4): Email (A), Event ID (G), Attended (T: `Yes` = presente, vuoto = no-show).
  - `RAW_CONTACTS` (riga 4): Email (A), Role (E), Submission Date (N), Event ID (R), Submission DateTime (W), Note (Y), **UTM (AB) = URL della landing con le UTM**. La colonna UTM esiste dal 9/11/2026 e Luigi ci ha spostato anche gli URL di Implantologia 2027; per i webinar precedenti (es. Marketing e Architettura) l'URL è in Note. Leggi prima UTM e, se è vuota, Note. Se l'intestazione non è più in AB, cercala per nome nella riga 4 (lo script di IDEHUB copia per posizione, quindi le colonne nuove vanno sempre in fondo).
  - `CONTACTS` (riga 4): Email (A), Create Date (N), Lifecycle Stage (V: Lead, Opportunity, Customer, Ex Customer).
  - Scarica i fogli interi con get_values (es. `EVENTS!A4:AD5000`): il risultato viene salvato su file; elaboralo in Python, mai a mano.
- **Meta**: account `113096912423590`, campagna `52600961859122`. Livello annuncio, filtra per nome del webinar (data o nome breve), `date_preset` maximum: spesa e risultati (evento pixel "Webinar") per annuncio e gruppo. Gruppo del webinar = remarketing; gruppo `52602074974122` "Webinar – Nuovo pubblico" = pubblico freddo; "Webinar – Caldo (condiviso)" se presente.

#### Calcoli

1. **Iscritti** = righe di EVENTS con l'event_id (email uniche). Escludi le iscrizioni doppie con email sbagliata (refusi come gnail.com, .con, dominio troncato).
2. **Partecipanti** = Attended `Yes`; il resto è no-show (dichiaralo nella nota delle fonti).
3. **Canale di ogni iscritto** dall'URL nella colonna UTM (o Note per i webinar più vecchi; se una persona ha più righe, vale la prima con un canale riconoscibile):
   - `utm_source=newsletter` → Newsletter (`utm_content` o `utm_campaign` dicono quale invio)
   - `utm_term` = ID del gruppo Meta (o `utm_medium` = `remarketing` / `freddo`) → Meta – Remarketing / Meta – Pubblico nuovo
   - `utm_source=whatsapp` → WhatsApp; `utm_medium=partner` → Partner; `utm_medium=organico` → Social organici; `utm_source=sito-ideandum` o `sito` → Sito
   - solo `fbclid` senza UTM → Facebook/Instagram senza UTM; URL vuoto → Non tracciato
   - URL della landing senza UTM e senza fbclid → Link senza UTM (link condiviso a mano o indirizzo scritto): va in Altri canali.
   - Se un canale è già stato indicato da Luigi nella scheda del webinar (es. elenco delle email arrivate dalla newsletter), usa quello per le iscrizioni senza URL.
   - **Se le colonne UTM e Note sono vuote per quasi tutti** (UTM o Zap mancanti), non inventare canali: usa per Meta le iscrizioni attribuite dal pixel, metti newsletter e altri canali insieme, segna "n.d." dove non si può sapere e metti in cima all'infografica un avviso "Dati per canale parziali". Segnala il problema a Luigi.
4. **Nuovi in IDEHUB** = contatto con Create Date in CONTACTS uguale (non precedente) alla data di iscrizione e nessuna riga precedente in RAW_CONTACTS. Prima di contarlo nuovo, cerca un contatto più vecchio con la stessa parte prima della @ o con un refuso evidente: se c'è, non è nuovo.
5. **Costi Meta**: spesa per gruppo solo sugli annunci di questo webinar; € per iscritto e € per partecipante di ogni gruppo con iscritti e partecipanti di IDEHUB; nella colonna Totale i costi si calcolano solo sugli iscritti e partecipanti arrivati da Meta (segnalo con un asterisco e una nota).
6. **Clienti tra gli iscritti** dal Lifecycle Stage: clienti attivi, ex clienti, trattative aperte (Opportunity), lead; iscritti e partecipanti per ciascuno, con il canale dei clienti se noto.
7. **Chi si presenta di più**: % di partecipazione dei contatti già presenti in IDEHUB contro quella dei nuovi.
8. **Confronto** con i webinar precedenti: prendi i valori dal foglio di confronto (iscritti, % partecipazione, % nuovi, spesa Meta, € per iscritto Meta).

Prima di scrivere l'infografica, mostra a Luigi in chat i numeri principali in tabella e i casi dubbi (refusi, iscritti senza canale, dati mancanti).

#### Foglio di confronto e dashboard (andamento tra webinar)

Dopo i calcoli, aggiorna la riga del webinar nel foglio Google "Webinar Ideandum – Confronto performance" (`1cXHQbG2YKcJTYUNcYBnJgq18IIKg-qZVvUmC7KdmOxc`, scheda `Webinar`). Ogni webinar ha una riga con l'Event ID in colonna A; se manca, aggiungila in fondo copiando le formule della riga sopra.

- **Colonne con formula, da non toccare**: B Data, C Webinar, D Stato, E Iscritti, F Partecipanti, G % partecipazione, H No-show, J % iscritti nuovi, L % partecipanti nuovi, O € per iscritto Meta, Q € per partecipante Meta. Iscritti e partecipanti arrivano da IDEHUB tramite la scheda `IDEHUB EVENTS` (IMPORTRANGE): se sono vuoti, ricorda a Luigi di cliccare "Consenti accesso" in quella scheda.
- **Colonne in blu da compilare**: numeri in I Iscritti nuovi in IDEHUB, K Partecipanti nuovi in IDEHUB, M Spesa Meta (€), N Iscritti da Meta, P Partecipanti da Meta, R Iscritti da newsletter, S Partecipanti da newsletter, T Iscritti da altri canali, V Clienti tra gli iscritti; testo in U Tracciamento canali ("Completo (UTM in IDEHUB)", "Parziale: …" o "Assente: …") e W Note (limiti dei dati, doppioni, differenze con Zoom).
- Il foglio è in locale italiano: nelle formule il separatore è `;`. Scrivi i valori con update_values e rileggi la riga per controllare.
- La dashboard "Webinar Ideandum – Andamento" (https://claude.ai/artifact/PGBoyw45ErCwMM2TiedMc1) legge il foglio da sola: non va modificata. Nel messaggio finale dai il link e una riga su come il webinar si confronta con il precedente (iscritti, % partecipazione, % nuovi, € per iscritto Meta).

#### Infografica (tipo di artifact Design, una per webinar)

Titolo del canvas: "Webinar <Nome> – Risultati". Immagine verticale larga 1080 px, sfondo #F5F6F8, titoli Space Grotesk, testo Inter. Colori fissi dei canali: Meta – Remarketing #1F4E9A, Meta – Pubblico nuovo #8DB0E3, Newsletter #D9661F, Altri canali #A7AFBA (altri canali con colori nuovi ma ben distinguibili). Ordine delle sezioni:

1. **Intestazione**: "Webinar · <data> · Report campagna", titolo del webinar, una riga di sottotitolo.
2. **Tabella "I numeri per canale"**, subito sotto il titolo: colonne = canali di acquisizione + Totale (sfondo grigio); righe in due blocchi separati, ognuno con la sua barra scura: **Iscrizioni** (Spesa, Totale iscritti, di cui nuovi in IDEHUB, € per iscritto) e **Partecipazione** (Totale partecipanti, di cui nuovi in IDEHUB, € per partecipante). Le righe dei nuovi sono evidenziate in arancione chiaro (#FDF1E8, testo #A9490C), con il numero grande e la percentuale piccola sotto, calcolata sul totale della stessa colonna. Nota sotto la tabella sui costi totali (solo Meta).
3. **Clienti Ideandum tra gli iscritti**: tre riquadri (clienti attivi, ex clienti, trattative aperte) con iscritti e partecipanti, più una riga sui lead.
4. **Quattro numeri chiave**: iscritti (con l'obiettivo di 100), partecipanti (con %), no-show (con %), spesa Meta (con € per iscritto Meta).
5. **Sezione 1 "Da dove arrivano le iscrizioni"**: torta degli iscritti per canale; in legenda, sotto ogni canale, "X su Y nuovi, non presenti prima su IDEHUB" con la % in piccolo; riquadro "Meta porta N iscritti su T a un costo medio di …"; riquadro scuro con i nuovi contatti generati e quanti hanno partecipato (anche per canale); confronto Meta remarketing / pubblico nuovo (spesa, iscritti, € per iscritto) con una frase di commento.
6. **Sezione 2 "Chi ha partecipato, per canale"**: torta dei partecipanti per canale; in legenda, sotto ogni canale, "N partecipanti su M iscritti · X su 10" (solo numeri); tabella "Partecipanti nuovi o già in IDEHUB" per canale con riga Totale; "Chi si presenta di più?" (due riquadri: % di partecipazione dei già presenti e dei nuovi, con "N su M iscritti") e una frase di sintesi; riquadri su newsletter e costo per partecipante.
7. **Conclusioni** (blocco scuro): due riquadri in evidenza, "persone nuove raggiunte" (X su totale iscritti, % piccola) e "persone nuove che hanno partecipato" (X su totale partecipanti, % piccola), poi 4 punti brevi con le indicazioni pratiche.
8. **Confronto** con i webinar precedenti (tabella piccola), se ce ne sono.
9. **Nota delle fonti** in fondo: fonti, data dei dati, come sono contati no-show, nuovi, doppioni, attribuzione Meta ed eventuali limiti (es. Advantage+ Audience attivo nel remarketing).

Regole: niente numeri inventati o stimati senza dirlo; percentuali con una cifra decimale nei testi, intere nelle righe dei nuovi; dove un dato manca scrivi "n.d." e spiega perché. Dopo la pubblicazione rispondi con 2-3 righe sui risultati principali, senza ripetere l'infografica. Se nel report mancano dati per canale, ricorda a Luigi che ogni link alla landing deve avere le UTM (sezione 1, "UTM su tutti i link").

