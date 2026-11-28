
from strumenti.comandi import crea_cartelle, esegui_comando


def test_vufs_merge(ambiente_virtuale, tmp_path):

    # 1. Creiamo le due cartelle
    crea_cartelle(tmp_path, "origine", "destinazione")

    cartella_origine = tmp_path / "origine"
    cartella_destinazione = tmp_path / "destinazione"

    # 2. Creiamo i file nelle due cartelle
    (cartella_origine / "a.txt").write_text("FILE A")
    (cartella_destinazione / "b.txt").write_text("FILE B")

    # Due file con lo stesso nome ma contenuti diversi
    (cartella_origine / "comune.txt").write_text("VERSIONE A")
    (cartella_destinazione / "comune.txt").write_text("VERSIONE B")

    # 3. Carichiamo VUFS
    assert esegui_comando(
        ambiente_virtuale, "vu_insmod vufs"
    ) == 0

    # 4. Eseguiamo il montaggio merge
    comando = f"vumount -t vufs -o merge {cartella_origine} {cartella_destinazione}"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 5. Entrambi i file devono essere visibili
    assert esegui_comando(
        ambiente_virtuale,
        f"test -f {cartella_destinazione}/a.txt"
    ) == 0

    assert esegui_comando(
        ambiente_virtuale,
        f"test -f {cartella_destinazione}/b.txt"
    ) == 0

    # 6. In caso di conflitto prevale il file di origine
    assert esegui_comando(
        ambiente_virtuale,
        f"cmp -s {cartella_origine}/comune.txt {cartella_destinazione}/comune.txt"
    ) == 0

    # 7. Fuori da UMVU il file originale non è cambiato
    assert (cartella_destinazione / "comune.txt").read_text() == "VERSIONE B"


def test_vufs_merge_scrittura(ambiente_virtuale, tmp_path):

    # 1. Creiamo le due cartelle
    crea_cartelle(tmp_path, "origine", "destinazione")

    cartella_origine = tmp_path / "origine"
    cartella_destinazione = tmp_path / "destinazione"

    # 2. Carichiamo il modulo VUFS
    assert esegui_comando(
        ambiente_virtuale, "vu_insmod vufs"
    ) == 0

    # 3. Eseguiamo il montaggio merge
    comando = f"vumount -t vufs -o merge {cartella_origine} {cartella_destinazione}"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 4. Creiamo un file nella destinazione virtuale
    comando = f"printf 'NUOVO' > {cartella_destinazione}/nuovo.txt"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 5. Verifichiamo che il file sia visibile in UMVU
    comando = f"test -f {cartella_destinazione}/nuovo.txt"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 6. Fuori da UMVU verifichiamo dove si trova il file
    assert (cartella_destinazione / "nuovo.txt").read_text() == "NUOVO"

    assert not (cartella_origine / "nuovo.txt").exists()
