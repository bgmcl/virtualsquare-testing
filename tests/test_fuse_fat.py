import pytest
from strumenti.comandi import esegui_comando, crea_cartelle


@pytest.mark.parametrize("opzioni", ["-s -o rw+", "-o rw+"])
def test_fuse_fat_base(ambiente_virtuale, tmp_path, opzioni):

    # 1. Prepariamo il disco e il montaggio
    disco = tmp_path / "disco.img"
    montaggio = tmp_path / "montaggio"

    crea_cartelle(tmp_path, "montaggio")

    # 2. Creiamo il disco virtuale da 10 MB
    assert esegui_comando(
        ambiente_virtuale,
        f"truncate -s 10M {disco}"
    ) == 0

    # 3. Formattiamo il disco FAT
    assert esegui_comando(
        ambiente_virtuale,
        f"/usr/sbin/mkfs.vfat {disco}"
    ) == 0

    # 4. Carichiamo il modulo FUSE
    assert esegui_comando(
        ambiente_virtuale, "vu_insmod fuse"
    ) == 0

    # 5. Montiamo il disco
    assert esegui_comando(
        ambiente_virtuale,
        f"fusefatfs {opzioni} {disco} {montaggio}"
    ) == 0

    try:
        # 6. Scriviamo un file
        assert esegui_comando(
            ambiente_virtuale,
            f"echo ciao > {montaggio}/ciao.txt"
        ) == 0

        # 7. Verifichiamo il contenuto
        assert esegui_comando(
            ambiente_virtuale,
            f"grep -Fxq ciao {montaggio}/ciao.txt"
        ) == 0

    finally:
        # 8. Smontiamo il filesystem
        assert esegui_comando(
            ambiente_virtuale,
            f"vuumount {montaggio}"
        ) == 0

def test_vufuse_fat_sola_lettura(ambiente_virtuale, tmp_path):

    # 1. Prepariamo il disco e il montaggio
    disco = tmp_path / "disco.img"
    montaggio = tmp_path / "montaggio"

    crea_cartelle(tmp_path, "montaggio")

    # 2. Creiamo e formattiamo il disco FAT
    assert esegui_comando(
        ambiente_virtuale,
        f"truncate -s 10M {disco}"
    ) == 0

    assert esegui_comando(
        ambiente_virtuale,
        f"/usr/sbin/mkfs.vfat {disco}"
    ) == 0

    # 3. Carichiamo il modulo vufuse
    assert esegui_comando(
        ambiente_virtuale, "vu_insmod vufuse"
    ) == 0

    # 4. Montiamo il disco in sola lettura
    assert esegui_comando(
        ambiente_virtuale,
        f"vumount -t vufusefatfs -o ro {disco} {montaggio}"
    ) == 0

    try:
        # 5. Il filesystem deve essere leggibile
        assert esegui_comando(
            ambiente_virtuale,
            f"ls {montaggio}"
        ) == 0

        # 6. La creazione di un file deve fallire
        assert esegui_comando(
            ambiente_virtuale,
            f"touch {montaggio}/prova.txt"
        ) != 0

        # 7. Il file non deve essere stato creato
        assert esegui_comando(
            ambiente_virtuale,
            f"test ! -e {montaggio}/prova.txt"
        ) == 0

    finally:
        # 8. Smontiamo il filesystem
        assert esegui_comando(
            ambiente_virtuale,
            f"vuumount {montaggio}"
        ) == 0
