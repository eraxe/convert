import polib

def po_to_txt(po_file, txt_file):
    po = polib.pofile(po_file)

    with open(txt_file, "w") as file:
        for entry in po:
            if entry.msgstr_plural:
                msgstr = entry.msgstr_plural.get(1, "")
            else:
                msgstr = entry.msgstr
            file.write(f"{entry.msgid} -> {msgstr}\n")




def txt_to_po(txt_file, output_file=None):
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

    if output_file:
        po.save(output_file)
    else:
        return str(po)