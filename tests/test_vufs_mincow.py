from strumenti.comandi import crea_cartelle, esegui_comando


def test_vufs_mincow_scrittura_consentita(ambiente_virtuale, tmp_path):

    # 1. Creiamo le cartelle A e B
    crea_cartelle(tmp_path, "copie", "originali")

    cartella_copie = tmp_path / "copie"
    cartella_originali = tmp_path / "originali"

    # 2. Creiamo un file originale scrivibile
    file_originale = cartella_originali / "messaggio.txt"
    file_originale.write_text("ORIGINALE")

    # 3. Carichiamo VUFS
    assert esegui_comando(
        ambiente_virtuale, "vu_insmod vufs"
    ) == 0

    # 4. Attiviamo MINCOW
    comando = f"vumount -t vufs -o mincow {cartella_copie} {cartella_originali}"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 5. Modifichiamo il file dentro UMVU
    comando = f"printf 'MODIFICATO' > {file_originale}"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 6. Verifichiamo che B sia stato modificato
    assert file_originale.read_text() == "MODIFICATO"

    # 7. Verifichiamo che A non contenga una copia
    file_copia = cartella_copie / "messaggio.txt"

    assert not file_copia.exists()


def test_vufs_mincow_directory_non_scrivibile(ambiente_virtuale, tmp_path):

    # Prepariamo le cartelle
    crea_cartelle(tmp_path, "copie", "originali")

    cartella_copie = tmp_path / "copie"
    cartella_originali = tmp_path / "originali"

    # Impediamo la creazione di file nella cartella B
    cartella_originali.chmod(0o555)

    try:
        # Carichiamo VUFS
        assert esegui_comando(
            ambiente_virtuale, "vu_insmod vufs"
        ) == 0

        # Attiviamo MINCOW
        comando = f"vumount -t vufs -o mincow {cartella_copie} {cartella_originali}"

        assert esegui_comando(ambiente_virtuale, comando) == 0

        # Proviamo a creare un file dentro UMVU
        comando = f"printf 'NUOVO' > {cartella_originali}/nuovo.txt"

        assert esegui_comando(ambiente_virtuale, comando) == 0

        # Verifichiamo che il file sia stato creato in A
        file_copia = cartella_copie / "nuovo.txt"
        assert file_copia.read_text() == "NUOVO"

        # Verifichiamo che B sia rimasta invariata
        file_originale = cartella_originali / "nuovo.txt"
        assert not file_originale.exists()

    finally:
        # Ripristiniamo i permessi per la pulizia
        cartella_originali.chmod(0o755)


import os
import pytest


def test_vufs_mincow_file_sistema(ambiente_virtuale, tmp_path):

    # 1. Individuiamo il file di sistema da verificare
    file_reale = "/etc/protocols"

    # Non eseguiamo la prova se il file originale
    # potrebbe essere modificato direttamente
    if os.geteuid() == 0 or os.access(file_reale, os.W_OK):
        pytest.skip("Il file reale è scrivibile: prova non sicura")

    # 2. Salviamo il contenuto originale
    with open(file_reale, "rb") as file:
        contenuto_originale = file.read()

    # 3. Creiamo la cartella per le copie virtuali

    crea_cartelle(tmp_path, "copie")
    cartella_copie = tmp_path / "copie"


    # 4. Carichiamo VUFS
    assert esegui_comando(
        ambiente_virtuale, "vu_insmod vufs"
    ) == 0

    # 5. Montiamo il filesystem in modalità mincow
    comando = (
        "vumount -t vufs "
        f"-o mincow,except=/tmp,except=/proc {cartella_copie} /"
    )

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 6. Aggiungiamo una riga al file virtualizzato
    comando = (
        "printf '\\n# PROVA_VUFS_MINCOW\\n' >> /etc/protocols"
    )

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 7. Dentro UMVU la modifica deve essere visibile
    comando = "grep -Fq '# PROVA_VUFS_MINCOW' /etc/protocols"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 8. Fuori da UMVU il file reale deve essere invariato
    with open(file_reale, "rb") as file:
        assert file.read() == contenuto_originale

    # 9. La copia modificata deve trovarsi nella cartella A
    file_copia = cartella_copie / "etc" / "protocols"

    assert file_copia.is_file()
    assert b"# PROVA_VUFS_MINCOW" in file_copia.read_bytes()
