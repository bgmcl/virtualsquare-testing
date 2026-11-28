# VirtualSquare – Automated Unit Testing

## Descrizione

Suite di test automatici per verificare le funzionalità VirtualSquare e individuare regressioni, sviluppata a partire dagli script Python della pexpect_unit_test e dai tutorial della wiki ufficiale VirtualSquare.

Tecnologie: Python, pytest, pexpect, VUOS.

## Stato del progetto

| Componente | Test | Esito |
|---|---:|---|
| VUFS | 17 | 17 PASS |
| UNREAL | 1 | PASS con purelibc 1.0.10 |
| FUSE EXT2 | 3 | 3 PASS |
| FUSE FAT | 3 | 3 PASS |
| **Totale** | **24** | **24 PASS con purelibc 1.0.10** |

VUFS: test delle modalità `bind`, `merge`, `cow`, `mincow`, delle eccezioni, dei metadati e delle modifiche virtuali.

UNREAL: verifica dei livelli di virtualizzazione annidata.

FUSE EXT2 e FAT: test di montaggio, accesso e operazioni sui file, comprese le verifiche di accesso in sola lettura tramite VUFUSE.

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

Per eseguire tutti i test:

```bash
./run_tests.sh
```

In alternativa:

```bash
python -m pytest -v tests/
```

Per eseguire la suite con `purelibc 1.0.10`, specificare la directory che contiene la libreria aggiornata:

```bash
LD_LIBRARY_PATH="/percorso/alla/directory/purelibc" \
python -m pytest -v tests/
```

Nell'ambiente Debian standard sono stati verificati **23 PASS e 1 FAIL**, relativo al secondo livello di virtualizzazione UNREAL.

Il test UNREAL è stato verificato positivamente utilizzando `purelibc 1.0.10`.

**Risultato verificato: 18 passed.**

## Nota su UNREAL

Su Debian 13, purelibc 1.0.8-1+b1 impedisce il funzionamento del secondo livello `/unreal/unreal`.

Il problema è coerente con il [Debian Bug #1144141](https://bugs.debian.org/1144141).

Con purelibc 1.0.10, estratta localmente e utilizzata tramite `LD_LIBRARY_PATH`, il test passa senza modifiche al codice o ai pacchetti di sistema.

## Sviluppi previsti

La suite comprende attualmente i test VUFS, UNREAL e FUSE (EXT2 e FAT).

I prossimi sviluppi riguarderanno i tutorial della rete virtuale VDE e le ulteriori funzionalità VirtualSquare non ancora coperte.

Gli aggiornamenti saranno documentati attraverso commit Git e mediante diff o patch rispetto alla versione precedentemente sottoposta al docente.