import polib

def po_to_txt(po_file):
    po = polib.pofile(po_file)
    with open(f"{po_file}_output.txt", "w") as txt_file:
        for entry in po:
            if entry.msgid_plural:
                txt_file.write(f"{entry.msgid} -> {entry.msgstr[0]}\n")
                txt_file.write(f"{entry.msgid_plural} -> {entry.msgstr[1]}\n")
            else:
                txt_file.write(f"{entry.msgid} -> {entry.msgstr}\n")

def txt_to_po(txt_file):
    with open(txt_file, "r") as file:
        lines = file.readlines()

    po = polib.POFile()
    po.metadata = {"Content-Type": "text/plain; charset=utf-8"}

    for i in range(len(lines)):
        line = lines[i].strip()
        if line:
            msgid, msgstr = line.split(" -> ")
            entry = polib.POEntry(msgid=msgid, msgstr=msgstr)

            # Handle plural forms
            if i + 1 < len(lines) and lines[i + 1].startswith(msgid + "_plural"):
                i += 1
                plural_line = lines[i].strip()
                msgid_plural, msgstr_plural = plural_line.split(" -> ")
                entry.msgid_plural = msgid_plural.replace("_
