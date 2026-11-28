import os
import pytest
from strumenti.comandi import crea_cartelle, esegui_comando


def test_vufs_cancellazione_virtuale(ambiente_virtuale, tmp_path):

    # Il test deve essere eseguito come utente normale
    if os.geteuid() == 0:
        pytest.skip("Eseguire senza sudo")

    # 1. Prepariamo le cartelle A e B
    crea_cartelle(tmp_path, "copie", "originali")

    cartella_copie = tmp_path / "copie"
    cartella_originali = tmp_path / "originali"

    # 2. Creiamo il file originale in B
    file_originale = cartella_originali / "prova.txt"
    file_originale.write_text("ORIGINALE")

    # 3. Impediamo la cancellazione reale
    cartella_originali.chmod(0o555)

    try:
        # 4. Carichiamo VUFS
        assert esegui_comando(
            ambiente_virtuale, "vu_insmod vufs"
        ) == 0

        # 5. Attiviamo MINCOW
        comando = f"vumount -t vufs -o mincow {cartella_copie} {cartella_originali}"
        assert esegui_comando(ambiente_virtuale, comando) == 0

        # 6. Cancelliamo il file dentro UMVU
        comando = f"rm -f {file_originale}"
        assert esegui_comando(ambiente_virtuale, comando) == 0

        # 7. Dentro UMVU il file non deve più essere visibile
        comando = f"test ! -e {file_originale}"
        assert esegui_comando(ambiente_virtuale, comando) == 0

        # 8. Fuori da UMVU il file deve ancora esistere
        assert file_originale.read_text() == "ORIGINALE"

    finally:
        # Ripristiniamo i permessi della cartella
        cartella_originali.chmod(0o755)
