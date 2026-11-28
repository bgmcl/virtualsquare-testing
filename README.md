# VirtualSquare – Automated Unit Testing

## Descrizione

Suite di test automatici per verificare le funzionalità VirtualSquare e individuare regressioni, sviluppata a partire dagli script Python della pexpect_unit_test e dai tutorial della wiki ufficiale VirtualSquare.

Tecnologie: Python, pytest, pexpect, VUOS.

## Stato del progetto

| Componente | Test | Esito |
|---|---:|---|
| VUFS | 17 | PASS |
| UNREAL | 1 | PASS |
| **Totale** | **18** | **18 PASS** |

VUFS: test delle modalità `bind`, `merge`, `cow`, `mincow`, delle eccezioni, dei metadati e delle modifiche virtuali.

UNREAL: verifica dei livelli di virtualizzazione annidata.

Il dettaglio è riportato in `docs/matrice_test.md`.

## Struttura

- `tests/`: test automatici e fixture pytest
- `strumenti/`: funzioni di supporto
- `requirements.txt`: dipendenze Python
- `run_tests.sh`: script di esecuzione

## Ambiente verificato

- Debian 13 (Trixie), amd64
- Python 3.13.5
- pytest 9.2.0
- pexpect 4.9.0
- VUOS 0.9.2-1

## Installazione

```bash
sudo apt install python3 python3-venv python3-pip vuos
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Esecuzione

```bash
python -m pytest -v tests/
```

Per eseguire anche UNREAL con la libreria corretta:

```bash
LD_LIBRARY_PATH="$HOME/prova-purelibc/estratta/usr/lib/x86_64-linux-gnu" \
python -m pytest -v tests/
```

**Risultato verificato: 18 passed.**

## Nota su UNREAL

Su Debian 13, purelibc 1.0.8-1+b1 impedisce il funzionamento del secondo livello `/unreal/unreal`.

Il problema è coerente con il [Debian Bug #1144141](https://bugs.debian.org/1144141).

Con purelibc 1.0.10, estratta localmente e utilizzata tramite `LD_LIBRARY_PATH`, il test passa senza modifiche al codice o ai pacchetti di sistema.

## Sviluppi previsti

Estensione della suite ai filesystem FUSE (EXT2, FAT), alla rete virtuale VDE e agli altri tutorial VirtualSquare.