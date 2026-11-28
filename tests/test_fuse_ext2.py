
from strumenti.comandi import esegui_comando, crea_cartelle


def test_fuse_ext2_base(ambiente_virtuale, tmp_path):

    # 1. Prepariamo il disco e la cartella di montaggio
    disco = tmp_path / "disco.img"
    montaggio = tmp_path / "montaggio"

    crea_cartelle(tmp_path, "montaggio")

    # 2. Creiamo un disco virtuale da 10 MB
    assert esegui_comando(
        ambiente_virtuale,
        f"truncate -s 10M {disco}"
    ) == 0

    # 3. Formattiamo il disco EXT2
    assert esegui_comando(
        ambiente_virtuale,
        f"/usr/sbin/mkfs.ext2 -F {disco}"
    ) == 0

    # 4. Carichiamo il modulo FUSE
    assert esegui_comando(
        ambiente_virtuale, "vu_insmod fuse"
    ) == 0

    # 5. Montiamo il filesystem
    assert esegui_comando(
        ambiente_virtuale,
        f"fuse2fs -s -o fakeroot {disco} {montaggio}"
    ) == 0

    try:
        # 6. Scriviamo un file nel filesystem virtuale
        assert esegui_comando(
            ambiente_virtuale,
            f"echo ciao > {montaggio}/ciao.txt"
        ) == 0

        # 7. Verifichiamo il contenuto del file
        assert esegui_comando(
            ambiente_virtuale,
            f"grep -Fxq ciao {montaggio}/ciao.txt"
        ) == 0

    finally:
        # 8. Smontiamo anche se una verifica fallisce
        assert esegui_comando(
            ambiente_virtuale,
            f"vuumount {montaggio}"
        ) == 0

def test_fuse_ext2_copia_file(ambiente_virtuale, tmp_path):

    # 1. Prepariamo il disco, il file e il montaggio
    disco = tmp_path / "disco.img"
    file_originale = tmp_path / "originale.bin"
    montaggio = tmp_path / "montaggio"

    crea_cartelle(tmp_path, "montaggio")

    # 2. Creiamo e formattiamo il disco EXT2
    assert esegui_comando(
        ambiente_virtuale,
        f"truncate -s 10M {disco}"
    ) == 0

    assert esegui_comando(
        ambiente_virtuale,
        f"/usr/sbin/mkfs.ext2 -F {disco}"
    ) == 0

    # 3. Carichiamo FUSE e montiamo il disco
    assert esegui_comando(
        ambiente_virtuale, "vu_insmod fuse"
    ) == 0

    assert esegui_comando(
        ambiente_virtuale,
        f"fuse2fs -s -o fakeroot {disco} {montaggio}"
    ) == 0

    try:
        # 4. Creiamo un file di circa 2 MB
        assert esegui_comando(
            ambiente_virtuale,
            f"dd if=/dev/urandom of={file_originale} "
            "bs=1024 count=2000 status=none"
        ) == 0

        # 5. Copiamo il file nel filesystem EXT2
        assert esegui_comando(
            ambiente_virtuale,
            f"cp {file_originale} {montaggio}/copia.bin"
        ) == 0

        # 6. Verifichiamo che i due file siano identici
        assert esegui_comando(
            ambiente_virtuale,
            f"cmp -s {file_originale} {montaggio}/copia.bin"
        ) == 0

    finally:
        # 7. Smontiamo il filesystem
        assert esegui_comando(
            ambiente_virtuale,
            f"vuumount {montaggio}"
        ) == 0

def test_vufuse_ext2_sola_lettura(ambiente_virtuale, tmp_path):

    # 1. Prepariamo il disco e il montaggio
    disco = tmp_path / "disco.img"
    montaggio = tmp_path / "montaggio"

    crea_cartelle(tmp_path, "montaggio")

    # 2. Creiamo e formattiamo il disco EXT2
    assert esegui_comando(
        ambiente_virtuale,
        f"truncate -s 10M {disco}"
    ) == 0

    assert esegui_comando(
        ambiente_virtuale,
        f"/usr/sbin/mkfs.ext2 -F -q {disco}"
    ) == 0

    # 3. Carichiamo il modulo vufuse
    assert esegui_comando(
        ambiente_virtuale, "vu_insmod vufuse"
    ) == 0

    # 4. Montiamo EXT2 in sola lettura
    assert esegui_comando(
        ambiente_virtuale,
        f"vumount -t vufuse2fs -o ro {disco} {montaggio}"
    ) == 0

    try:
        # 5. Verifichiamo che il disco sia accessibile
        assert esegui_comando(
            ambiente_virtuale,
            f"test -d {montaggio}/lost+found"
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
