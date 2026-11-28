
from strumenti.comandi import esegui_comando, crea_cartelle


def test_vufs_bind_except(ambiente_virtuale, tmp_path):

    # 1. Creiamo le due cartelle
    crea_cartelle(tmp_path, "origine", "destinazione")

    cartella_origine = tmp_path / "origine"
    cartella_destinazione = tmp_path / "destinazione"

    # 2. Creiamo la sottocartella spool in entrambe
    crea_cartelle(cartella_origine, "spool")
    crea_cartelle(cartella_destinazione, "spool")


    # 3. Prepariamo i file di prova
    (cartella_origine / "virtuale.txt").write_text("VIRTUALE")

    (cartella_destinazione / "nascosto.txt").write_text("NASCOSTO")

    file_reale = cartella_destinazione / "spool" / "reale.txt"
    file_reale.write_text("REALE")

    # 4. Carichiamo VUFS
    assert esegui_comando(
        ambiente_virtuale, "vu_insmod vufs"
    ) == 0

    # 5. Montiamo BIND con l'eccezione spool
    comando = (
        f"vumount -t vufs -o bind,except=/spool "
        f"{cartella_origine} {cartella_destinazione}"
    )

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 6. Il file di A deve essere visibile in B
    comando = f"test -f {cartella_destinazione}/virtuale.txt"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 7. Il file originale di B deve essere nascosto
    comando = f"test ! -e {cartella_destinazione}/nascosto.txt"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 8. Il file nella sottocartella esclusa deve restare visibile
    comando = f"test -f {cartella_destinazione}/spool/reale.txt"

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 9. Fuori da UMVU i file originali restano invariati
    assert file_reale.read_text() == "REALE"

    assert (
        cartella_destinazione / "nascosto.txt"
    ).read_text() == "NASCOSTO"


def test_vufs_bind_due_eccezioni(ambiente_virtuale, tmp_path):

    # 1. Creiamo origine e destinazione
    crea_cartelle(tmp_path, "origine", "destinazione")

    cartella_origine = tmp_path / "origine"
    cartella_destinazione = tmp_path / "destinazione"

    # 2. Creiamo spool e proc in entrambe le cartelle
    for nome in ("spool", "proc"):
        crea_cartelle(cartella_origine, nome)
        crea_cartelle(cartella_destinazione, nome)

        # File presente solo nell'origine
        (cartella_origine / nome / "virtuale.txt").write_text(
            "VIRTUALE"
        )

        # File presente solo nella destinazione reale
        (cartella_destinazione / nome / "reale.txt").write_text(
            "REALE"
        )

    # 3. Creiamo file fuori dalle eccezioni
    (cartella_origine / "origine.txt").write_text("ORIGINE")
    (cartella_destinazione / "nascosto.txt").write_text("REALE")

    # 4. Carichiamo VUFS
    assert esegui_comando(
        ambiente_virtuale, "vu_insmod vufs"
    ) == 0

    # 5. Montiamo bind con DUE eccezioni
    comando = (
        f"vumount -t vufs -o bind,except=/spool,except=/proc "
        f"{cartella_origine} {cartella_destinazione}"
    )

    assert esegui_comando(ambiente_virtuale, comando) == 0

    # 6. Fuori dalle eccezioni, il bind deve funzionare
    assert esegui_comando(
        ambiente_virtuale,
        f"test -f {cartella_destinazione}/origine.txt"
    ) == 0

    assert esegui_comando(
        ambiente_virtuale,
        f"test ! -e {cartella_destinazione}/nascosto.txt"
    ) == 0

    # 7. Entrambe le eccezioni devono funzionare
    for nome in ("spool", "proc"):

        # Il file reale deve rimanere visibile
        assert esegui_comando(
            ambiente_virtuale,
            f"test -f {cartella_destinazione}/{nome}/reale.txt"
        ) == 0

        # Il file dell'origine non deve comparire
        assert esegui_comando(
            ambiente_virtuale,
            f"test ! -e {cartella_destinazione}/{nome}/virtuale.txt"
        ) == 0

    # 8. Fuori da UMVU, i file reali sono invariati
    for nome in ("spool", "proc"):
        assert (
            cartella_destinazione / nome / "reale.txt"
        ).read_text() == "REALE"

    assert (
        cartella_destinazione / "nascosto.txt"
    ).read_text() == "REALE"
