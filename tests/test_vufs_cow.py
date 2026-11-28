
from strumenti.comandi import crea_cartelle, esegui_comando


def test_vufs_cow_modifica(ambiente_virtuale, tmp_path):

    # 1. Prepariamo le cartelle

    crea_cartelle(tmp_path, "copie", "originali")

    cartella_copie = tmp_path / "copie"
    cartella_originali = tmp_path / "originali"


    # 2. Creiamo il file originale
    file_originale = cartella_originali / "messaggio.txt"
    file_originale.write_text("ORIGINALE")

    # 3. Carichiamo VUFS
    assert esegui_comando(
        ambiente_virtuale, "vu_insmod vufs"
    ) == 0

    # 4. Attiviamo la modalità COW
    comando = f"vumount -t vufs -o cow {cartella_copie} {cartella_originali}"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 5. Modifichiamo il file attraverso UMVU
    comando = f"printf 'MODIFICATO' > {file_originale}"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 6. Dentro UMVU vediamo il contenuto modificato
    comando = f"grep -qx MODIFICATO {file_originale}"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 7. Fuori da UMVU l'originale non deve cambiare
    assert file_originale.read_text() == "ORIGINALE"

    # 8. La copia deve contenere la modifica
    file_copia = cartella_copie / "messaggio.txt"

    assert file_copia.read_text() == "MODIFICATO"


def test_vufs_cow_creazione(ambiente_virtuale, tmp_path):

    # 1. Prepariamo le cartelle
    crea_cartelle(tmp_path, "copie", "originali")

    cartella_copie = tmp_path / "copie"
    cartella_originali = tmp_path / "originali"

    # 2. Carichiamo VUFS
    assert esegui_comando(
        ambiente_virtuale, "vu_insmod vufs"
    ) == 0

    # 3. Attiviamo COW
    comando = f"vumount -t vufs -o cow {cartella_copie} {cartella_originali}"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 4. Creiamo un file dentro UMVU
    comando = f"printf 'NUOVO' > {cartella_originali}/nuovo.txt"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 5. Verifichiamo che il file sia visibile in UMVU
    comando = f"test -f {cartella_originali}/nuovo.txt"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 6. Verifichiamo dove il file è stato salvato
    file_copia = cartella_copie / "nuovo.txt"
    file_originale = cartella_originali / "nuovo.txt"

    assert file_copia.read_text() == "NUOVO"
    assert not file_originale.exists()
