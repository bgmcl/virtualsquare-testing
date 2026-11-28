import os
import pytest
from pathlib import Path
from strumenti.comandi import crea_cartelle, esegui_comando


def test_vufs_chown_virtuale(ambiente_virtuale, tmp_path):

    # Non eseguiamo questo test come root
    if os.geteuid() == 0:
        pytest.skip("Eseguire il test senza sudo")

    # Scegliamo un file di sistema appartenente a root
    file_originale = Path("/etc/protocols")

    if not file_originale.is_file():
        pytest.skip("File /etc/protocols non disponibile")

    assert file_originale.stat().st_uid == 0

    # Prepariamo la cartella per le modifiche virtuali
    crea_cartelle(tmp_path, "copie")
    cartella_copie = tmp_path / "copie"

    # Carichiamo VUFS
    assert esegui_comando(
        ambiente_virtuale, "vu_insmod vufs"
    ) == 0

    # Virtualizziamo soltanto /etc
    comando = f"vumount -t vufs -o mincow {cartella_copie} /etc"
    assert esegui_comando(ambiente_virtuale, comando) == 0

    # Modifichiamo virtualmente il proprietario
    mio_uid = os.getuid()
    comando = f"chown {mio_uid} /etc/protocols"
    assert esegui_comando(ambiente_virtuale, comando) == 0

    # Dentro UMVU il proprietario deve essere il nostro utente
    comando = f'test "$(stat -c %u /etc/protocols)" -eq {mio_uid}'
    assert esegui_comando(ambiente_virtuale, comando) == 0

    # Fuori da UMVU il proprietario deve essere ancora root
    assert file_originale.stat().st_uid == 0


def test_vufs_chmod_virtuale(ambiente_virtuale, tmp_path):

    # 1. Verifichiamo di non essere root
    if os.geteuid() == 0:
        pytest.skip("Eseguire senza sudo")

    # 2. Individuiamo il file originale
    file_originale = Path("/etc/protocols")

    if not file_originale.is_file():
        pytest.skip("File non disponibile")

    # Il file deve appartenere a root
    assert file_originale.stat().st_uid == 0

    # Memorizziamo i suoi permessi reali
    permessi_originali = file_originale.stat().st_mode & 0o777

    if permessi_originali == 0o600:
        pytest.skip("Il file ha già i permessi 600")

    # 3. Prepariamo la directory delle copie

    crea_cartelle(tmp_path, "copie")
    cartella_copie = tmp_path / "copie"

    # 4. Carichiamo VUFS
    assert esegui_comando(
        ambiente_virtuale, "vu_insmod vufs"
    ) == 0

    # 5. Attiviamo MINCOW sulla directory /etc
    comando = f"vumount -t vufs -o mincow {cartella_copie} /etc"
    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 6. Modifichiamo virtualmente i permessi
    assert esegui_comando(
        ambiente_virtuale, "chmod 600 /etc/protocols"
    ) == 0

    # 7. Dentro UMVU i permessi devono essere 600
    comando = 'test "$(stat -c %a /etc/protocols)" = 600'
    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 8. Fuori da UMVU i permessi devono essere invariati
    assert (file_originale.stat().st_mode & 0o777) == permessi_originali
