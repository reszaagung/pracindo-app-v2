import re
from itertools import groupby


def algoritma_chunking(items, pola_pilihan=None):
    if pola_pilihan:
        return {"pola": pola_pilihan, "grup_per_item": list(dict.fromkeys(pola_pilihan))}

    jumlah = len(items)
    if jumlah == 1:
        return {"pola": "AAAA", "grup_per_item": ["A"]}
    elif jumlah == 2:
        return {"pola": "AABB", "grup_per_item": ["A", "B"]}
    elif jumlah == 3:
        return {"pola": "AABC", "grup_per_item": ["A", "B", "C"]}
    elif jumlah >= 4:
        return {"pola": "ABCD", "grup_per_item": ["A", "B", "C", "D"]}

    return {"pola": "AAAA", "grup_per_item": ["A"]}


def encode_pola(pola):
    """Ringkas pola jadi nama pendek untuk nama_file Master Data.
    Seragam -> "<jumlah_grup>x<ukuran>" (mis. AABBCCDDEEFF -> "6x2").
    Semua beda -> pola literal apa adanya (sudah pendek, paling jelas).
    Campur ukuran -> "A11-B" gaya (fallback, jaga-jaga)."""
    ukuran_grup = [sum(1 for _ in grup) for _, grup in groupby(pola)]
    jumlah_grup = len(ukuran_grup)

    if len(set(ukuran_grup)) == 1:
        ukuran = ukuran_grup[0]
        if ukuran == 1:
            return pola
        return f"{jumlah_grup}x{ukuran}"

    bagian = []
    for huruf, grup in groupby(pola):
        jumlah = sum(1 for _ in grup)
        bagian.append(huruf if jumlah == 1 else f"{huruf}{jumlah}")
    return "-".join(bagian)


def decode_pola(kode):
    """Kebalikan persis dari encode_pola."""
    cocok_seragam = re.fullmatch(r"(\d+)x(\d+)", kode)
    if cocok_seragam:
        jumlah_grup, ukuran = int(cocok_seragam.group(1)), int(cocok_seragam.group(2))
        return "".join(chr(65 + i) * ukuran for i in range(jumlah_grup))

    if "-" in kode:
        hasil = []
        for bagian in kode.split("-"):
            cocok = re.fullmatch(r"([A-Z])(\d*)", bagian)
            huruf, jumlah = cocok.group(1), int(cocok.group(2) or 1)
            hasil.append(huruf * jumlah)
        return "".join(hasil)

    return kode