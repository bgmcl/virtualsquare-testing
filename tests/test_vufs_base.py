from strumenti.comandi import esegui_comando


# TEST 1 - VERIFICA ESISTENZA FILE

def test_vufs_file_visibile(ambiente_virtuale):

    assert esegui_comando(
        ambiente_virtuale, "vu_insmod vufs"
    ) == 0

    assert esegui_comando(
        ambiente_virtuale, "vumount -t vufs / /unreal"
    ) == 0

    assert esegui_comando(
        ambiente_virtuale, "test -f /unreal/etc/passwd"
    ) == 0


# TEST 2 - DOPPIO MONTAGGIO VUFS

def test_vufs_doppio_montaggio(ambiente_virtuale):

    assert esegui_comando(
        ambiente_virtuale, "vu_insmod vufs"
    ) == 0

    assert esegui_comando(
        ambiente_virtuale, "vumount -t vufs / /unreal"
    ) == 0

    assert esegui_comando(
        ambiente_virtuale, "vumount -t vufs / /unreal"
    ) == 0

    assert esegui_comando(
        ambiente_virtuale,
        "test -f /unreal/etc/passwd"
    ) == 0

    assert esegui_comando(
        ambiente_virtuale,
        "test -f /unreal/unreal/etc/passwd"
    ) == 0

    assert esegui_comando(
        ambiente_virtuale,
        "test ! -e /unreal/unreal/unreal/etc/passwd"
    ) == 0


# TEST 3 - CONFRONTO CONTENUTO FILE

def test_vufs_contenuto_uguale(ambiente_virtuale):

    assert esegui_comando(
        ambiente_virtuale, "vu_insmod vufs"
    ) == 0

    assert esegui_comando(
        ambiente_virtuale, "vumount -t vufs / /unreal"
    ) == 0

    assert esegui_comando(
        ambiente_virtuale,
        "cmp -s /etc/passwd /unreal/etc/passwd"
    ) == 0
