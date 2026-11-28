
def esegui_comando(ambiente_virtuale, comando):
    ambiente_virtuale.sendline(f"{comando}; echo ESITO:$?")
    ambiente_virtuale.expect(r"ESITO:(\d+)")
    return int(ambiente_virtuale.match.group(1))

def crea_cartelle(cartella_base, *nomi):
    for nome in nomi:
        (cartella_base / nome).mkdir()