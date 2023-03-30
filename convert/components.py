import polib

def po_to_txt(input_filepath: str, output_filepath: str):
    po = polib.pofile(input_filepath)
    with open(output_filepath, "w", encoding="utf-8") as txt_file:
        for entry in po:
            txt_file.write(f"{entry.msgid} -> {entry.msgstr}\n")
            if entry.msgid_plural:
                txt_file.write(f"{entry.msgid_plural} -> ")
                for index, msgstr_plural in enumerate(entry.msgstr_plural):
                    if index > 0:
                        txt_file.write(", ")
                    txt_file.write(f"{index}: {msgstr_plural}")
                txt_file.write("\n")


def txt_to_po(txt_file):
    with open(txt_file, "r") as file:
        lines = file.readlines()

    po = polib.POFile()
    po.metadata = {"Content-Type": "text/plain; charset=utf-8"}

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line:
            msgid, msgstr = line.split(" -> ")
            entry = polib.POEntry(msgid=msgid, msgstr=msgstr)

            # Handle plural forms
            if i + 1 < len(lines) and lines[i + 1].startswith("%d"):
                i += 1
                plural_line = lines[i].strip()
                msgid_plural, msgstr_plural = plural_line.split(" -> ")
                entry.msgid_plural = msgid_plural
                entry.msgstr_plural = {0: msgstr, 1: msgstr_plural}

            po.append(entry)
        i += 1

    with open(f"{txt_file}_output.po", "w") as po_file:
        po_file.write(str(po))
