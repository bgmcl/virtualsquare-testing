# Matrice dei test VirtualSquare

| File | Funzionalità | Test | Esito |
|---|---|---:|---|
| `test_vufs_base.py` | Visibilità, doppio montaggio, contenuto | 3 | PASS |
| `test_vufs_bind.py` | Bind e scrittura | 2 | PASS |
| `test_vufs_merge.py` | Merge, scrittura e precedenza | 2 | PASS |
| `test_vufs_cow.py` | Modifica e creazione virtuale | 2 | PASS |
| `test_vufs_mincow.py` | Scrittura e modifica virtuale file di sistema | 3 | PASS |
| `test_vufs_except.py` | Eccezione singola e doppia | 2 | PASS |
| `test_vufs_metadati.py` | Chown e chmod virtuali | 2 | PASS |
| `test_vufs_cancellazione.py` | Cancellazione virtuale | 1 | PASS |
| `test_unreal.py` | Virtualizzazione annidata | 1 | PASS |
| `test_fuse_ext2.py` | EXT2: lettura/scrittura, copia file, VUFUSE sola lettura | 3 | PASS |
| `test_fuse_fat.py` | FAT: single/multithread, VUFUSE sola lettura | 3 | PASS |
| **Totale** | | **24** | **PASS** |

## Ambiente

Debian 13, VUOS 0.9.2-1, Python 3.13.5.

- UNREAL: purelibc 1.0.10 tramite `LD_LIBRARY_PATH`.
- VUFUSE EXT2: modulo `vufuse2fs.so` compilato dai sorgenti.

## Copertura

- **VUFS:** completati i casi individuati nel tutorial.
- **UNREAL:** verificato l'esempio dell'autovirtualizzazione.
- **FUSE:** verificati gli esempi EXT2 e FAT e i montaggi VUFUSE.
- **Da sviluppare:** VDE e ulteriori tutorial VirtualSquare.

Riferimento: [VirtualSquare Wiki](https://wiki.virtualsquare.org/).
