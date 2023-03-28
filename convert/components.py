import polib

def po_to_txt(po_filepath: str, txt_filepath: str):
    po = polib.pofile(po_filepath)
    with open(txt_filepath, "w") as txt_file:
        for entry in po:
            txt_file.write(f"{entry.msgid} -> {entry.msgstr}\n")
