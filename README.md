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

## Ambiente utilizzato

- Sistema operativo: Debian
- Python: 3.13.5
- pytest: 9.2.0
- Libreria pexpect
- UMVU e modulo VUFS di VirtualSquare

## Installazione delle dipendenze Python

Dalla directory principale del progetto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

I componenti VirtualSquare devono essere già installati e disponibili nell'ambiente di esecuzione. Le relative istruzioni di installazione saranno documentate nelle versioni successive.

## Esecuzione dei test

Per avviare tutti i test della suite:

```bash
python -m pytest tests/ -v
```

Per eseguire soltanto i test VUFS:

```bash
python -m pytest tests/test_vufs_base.py -v
```

## Risultati della verifica iniziale

Ambiente: Debian, Python 3.13.5, pytest 9.2.0.

```text
test_vufs_file_visibile     PASSED
test_vufs_doppio_montaggio  PASSED
test_vufs_contenuto_uguale  PASSED

3 passed in 1.08s
```

Il risultato documenta l'esecuzione locale della suite e non garantisce ancora la riproducibilità su ambienti differenti.

## Sviluppi previsti

Il progetto sarà ampliato progressivamente per verificare ulteriori funzionalità VUFS e altri componenti VirtualSquare, seguendo i rispettivi tutorial.

Le modifiche saranno registrate attraverso Git, consentendo di confrontare le successive versioni del progetto e individuare con precisione il codice aggiunto o modificato.
