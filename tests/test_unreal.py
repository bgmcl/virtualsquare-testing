# Test del modulo UNREAL di VUOS.
#
# Su Debian 13 con VUOS 0.9.2-1 e purelibc 1.0.8,
# il secondo livello /unreal/unreal non funziona.
#
# Il problema si risolve nel nostro ambiente di prova
# utilizzando purelibc 1.0.10 tramite LD_LIBRARY_PATH.
#
# Il test è passato senza modifiche al codice Python.
# Per maggiori dettagli consultare il README.md.

from strumenti.comandi import esegui_comando


def test_unreal_due_livelli(ambiente_virtuale):

    # 1. Carichiamo il modulo UNREAL
    assert esegui_comando(
        ambiente_virtuale, "vu_insmod unreal"
    ) == 0

    # 2. Verifichiamo il primo livello virtualizzato
    assert esegui_comando(
        ambiente_virtuale,
        "test -f /unreal/etc/passwd"
    ) == 0

    # 3. Verifichiamo il secondo livello virtualizzato
    assert esegui_comando(
        ambiente_virtuale,
        "test -f /unreal/unreal/etc/passwd"
    ) == 0

    # 4. Il terzo livello NON deve esistere
    assert esegui_comando(
        ambiente_virtuale,
        "test ! -e /unreal/unreal/unreal/etc/passwd"
    ) == 0
