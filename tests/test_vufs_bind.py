
from strumenti.comandi import esegui_comando, crea_cartelle


def test_vufs_bind(ambiente_virtuale, tmp_path):

    # 1. Prepariamo due cartelle di prova
    crea_cartelle(tmp_path, "origine", "destinazione")

    cartella_origine = tmp_path / "origine"
    cartella_destinazione = tmp_path / "destinazione"

    # 2. Creiamo un file in ciascuna cartella
    (cartella_origine / "sorgente.txt").write_text("CIAO")
    (cartella_destinazione / "originale.txt").write_text("ORIGINALE")

    # 3. Carichiamo VUFS
    assert esegui_comando(
        ambiente_virtuale, "vu_insmod vufs"
    ) == 0

    # 4. Montiamo origine su destinazione
    comando = f"vumount -t vufs -o bind {cartella_origine} {cartella_destinazione}"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 5. Il file di origine deve essere visibile
    comando = f"test -f {cartella_destinazione}/sorgente.txt"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 6. Il file originale deve essere nascosto
    comando = f"test ! -e {cartella_destinazione}/originale.txt"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 7. Fuori da UMVU il file originale deve esistere
    assert (cartella_destinazione / "originale.txt").read_text() == "ORIGINALE"


def test_vufs_bind_scrittura(ambiente_virtuale, tmp_path):

    # 1. Prepariamo le due cartelle
    crea_cartelle(tmp_path, "origine", "destinazione")

    cartella_origine = tmp_path / "origine"
    cartella_destinazione = tmp_path / "destinazione"

    # 2. Creiamo un file originale in B
    file_originale = cartella_destinazione / "originale.txt"
    file_originale.write_text("ORIGINALE")

    # 3. Carichiamo VUFS
    assert esegui_comando(
        ambiente_virtuale, "vu_insmod vufs"
    ) == 0

    # 4. Attiviamo BIND
    comando = f"vumount -t vufs -o bind {cartella_origine} {cartella_destinazione}"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 5. Creiamo un nuovo file attraverso B
    comando = f"printf 'NUOVO' > {cartella_destinazione}/nuovo.txt"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 6. Dentro UMVU il nuovo file deve essere visibile
    comando = f"test -f {cartella_destinazione}/nuovo.txt"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 7. Fuori da UMVU il nuovo file deve trovarsi in A
    file_creato = cartella_origine / "nuovo.txt"

    assert file_creato.read_text() == "NUOVO"

    # 8. B non deve contenere fisicamente il nuovo file
    assert not (cartella_destinazione / "nuovo.txt").exists()

    # 9. Il file originale in B deve essere rimasto intatto
    assert file_originale.read_text() == "ORIGINALE"
