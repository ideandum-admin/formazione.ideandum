# Pubblicazione automatica di formazione.ideandum.com — istruzioni per il webmaster

Tempo richiesto: circa 10–15 minuti, una volta sola.

## Cosa fa

Il repository GitHub `ideandum-hub/formazione.ideandum` contiene le pagine del sottodominio.
A ogni modifica del branch `main`, GitHub carica via FTP **solo i file cambiati** sul server.

- I file già presenti sul server e **non** presenti nel repository **non vengono toccati né cancellati**:
  le landing esistenti restano online come sono.
- La cartella `_assets/` del repository contiene gli stessi file di quella attuale sul server:
  al primo caricamento verranno sovrascritti con copie identiche.

## 1. Installare l'app Claude su GitHub

Per permettere a Claude di scrivere nel repository:

1. Apri https://github.com/apps/claude/installations/select_target
2. Scegli l'organizzazione **ideandum-hub**.
3. In "Repository access" includi **formazione.ideandum** (o tutti i repository).
4. Salva.

Se l'app è già installata sull'organizzazione, basta aggiungere `formazione.ideandum` all'elenco dei repository.

## 2. Inserire le credenziali FTP come segreti

Su GitHub: **repository → Settings → Secrets and variables → Actions → New repository secret**.
Crea questi segreti (i valori non saranno più visibili, neanche a Claude):

| Nome | Valore |
|---|---|
| `FTP_SERVER` | host FTP, es. `ftp.ideandum.com` |
| `FTP_USERNAME` | utente FTP (meglio un utente dedicato, limitato alla cartella del sottodominio) |
| `FTP_PASSWORD` | password FTP |
| `FTP_SERVER_DIR` | cartella del sottodominio sul server, **con `/` finale**, es. `/formazione.ideandum.com/` |
| `FTP_PROTOCOL` | facoltativo: `ftps` (predefinito) oppure `ftp` se il server non supporta FTPS |

⚠️ Verificare con attenzione `FTP_SERVER_DIR`: è la cartella che contiene oggi `_assets/` e `grazie-webinar/`.

## 3. Collaudo

1. Su GitHub apri la scheda **Actions → Pubblica sito → Run workflow**.
2. Al termine (icona verde) apri https://formazione.ideandum.com/test-pubblicazione/
3. Se vedi "Pubblicazione automatica funzionante", è tutto a posto.

Se il job fallisce, il log nella scheda Actions indica il motivo (di solito host, cartella o protocollo).

## Note di sicurezza

- Le credenziali restano solo nei segreti di GitHub; non sono nel codice.
- Il caricamento esclude i file di lavoro (`_template/`, `scripts/`, `data/`, `.github/`, questi documenti).
