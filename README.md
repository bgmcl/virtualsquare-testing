# VirtualSquare – Automated Unit Testing

## Descrizione

Il progetto ha l'obiettivo di sviluppare una suite di test automatici per verificare il corretto funzionamento delle funzionalità dei sistemi VirtualSquare, con particolare riferimento agli esempi e ai tutorial pubblicati nella [wiki ufficiale VirtualSquare](https://wiki.virtualsquare.org/).

I test sono realizzati in Python utilizzando `pytest` e `pexpect`, con l'obiettivo di individuare eventuali regressioni a seguito di modifiche ai componenti del sistema.

## Stato di avanzamento

La prima versione del progetto comprende tre test relativi al filesystem virtuale VUFS:

| Test | Verifica |
|---|---|
| `test_vufs_file_visibile` | Verifica che un file sia accessibile attraverso il filesystem virtualizzato |
| `test_vufs_doppio_montaggio` | Verifica il comportamento di due montaggi virtuali |
| `test_vufs_contenuto_uguale` | Verifica la corrispondenza del contenuto dei file |

I tre test sono stati eseguiti con esito positivo nell'ambiente di sviluppo.

## Struttura del progetto

```text
virtualsquare-testing/
├── strumenti/
│   ├── __init__.py
│   └── comandi.py
├── tests/
│   ├── conftest.py
│   └── test_vufs_base.py
├── requirements.txt
├── README.md
└── .gitignore
```

La directory `strumenti` contiene le funzioni di supporto riutilizzabili. La directory `tests` contiene i test automatici e le fixture di pytest.

## Ambiente di sviluppo verificato

Il progetto è stato sviluppato e verificato con la seguente configurazione:

- Sistema operativo: Debian 13 (Trixie), amd64
- Python: 3.13.5
- pytest: 9.2.0
- pexpect: 4.9.0
- VUOS: 0.9.2-1

Pacchetti Debian utilizzati:
- `vuos`
- `vuos-umvu`
- `vuos-cmds`
- `vuos-modules`

## Installazione dei prerequisiti

Su Debian 13, installare Python e VirtualSquare:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip vuos
```

Verificare che i comandi di VirtualSquare siano disponibili:

```bash
command -v umvu
command -v vu_insmod
command -v vumount
```

## Installazione delle dipendenze Python

Dalla directory principale del progetto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Esecuzione dei test

Per eseguire tutti i test:

```bash
./run_tests.sh
```

In alternativa:

```bash
python -m pytest tests/ -v
```

Per eseguire soltanto i test VUFS:

```bash
python -m pytest tests/test_vufs_base.py -v
```

## Risultati della verifica iniziale

I test sono stati eseguiti su Debian 13 con Python 3.13.5, pytest 9.2.0 e VUOS 0.9.2-1.

```text
test_vufs_file_visibile     PASSED
test_vufs_doppio_montaggio  PASSED
test_vufs_contenuto_uguale  PASSED

3 passed in 1.08s
```

I risultati si riferiscono all'ambiente di sviluppo verificato. L'esecuzione su altri sistemi richiede la disponibilità dei componenti VirtualSquare e delle dipendenze indicate.

## Sviluppi previsti

Il progetto sarà ampliato progressivamente per verificare ulteriori funzionalità VUFS e altri componenti VirtualSquare, seguendo i tutorial ufficiali.

Le modifiche saranno registrate attraverso Git, consentendo di confrontare le versioni successive del progetto.
