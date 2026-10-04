import json
from pathlib import Path

# ============================================================
# KONFIGURASI
# ============================================================

ROOT = Path(".").resolve()
OUTPUT = ROOT / "komik.json"

EXCLUDE_DIRS = {
    ".git",
    ".github",
    "node_modules",
}

TARGET_FILE = "halaman-00.jpg"

# ============================================================
# INFORMASI ROOT
# ============================================================

print("=" * 70)
print("GENERATE DAFTAR KOMIK")
print("=" * 70)

print("ROOT :", ROOT)
print("TARGET:", TARGET_FILE)
print()

# ============================================================
# CEK FOLDER MTK
# ============================================================

mtk_folder = ROOT / "mtk"

print("CEK FOLDER MTK")
print("-" * 70)

if mtk_folder.exists():
    print("Folder mtk ditemukan.")

    if mtk_folder.is_dir():
        print("Status : folder")
    else:
        print("Status : BUKAN folder")

    print()

    print("Isi folder mtk:")

    for item in mtk_folder.rglob("*"):

        if item.is_file():
            relative = item.relative_to(ROOT)

            print(
                "  -",
                relative.as_posix()
            )

else:
    print("!!! FOLDER MTK TIDAK DITEMUKAN !!!")

print()

# ============================================================
# MENCARI SEMUA halaman-00.jpg
# ============================================================

hasil = []

print("=" * 70)
print("MENCARI halaman-00.jpg")
print("=" * 70)
print()

for file in ROOT.rglob("*"):

    if not file.is_file():
        continue

    if any(part in EXCLUDE_DIRS for part in file.parts):
        continue

    relative_path = file.relative_to(ROOT)

    # --------------------------------------------------------
    # TAMPILKAN FILE YANG BERADA DI MTK
    # --------------------------------------------------------

    if relative_path.as_posix().lower().startswith("mtk/"):

        print(
            "FILE MTK:",
            relative_path.as_posix()
        )

    # --------------------------------------------------------
    # PERIKSA NAMA FILE
    # --------------------------------------------------------

    if file.name.lower() != TARGET_FILE.lower():
        continue

    folder = relative_path.parent

    if not folder.parts:
        continue

    mapel = folder.parts[0]

    nama_komik = folder.name

    item = {
        "mapel": mapel,
        "folder": folder.as_posix(),
        "path": relative_path.as_posix(),
        "file": file.name,
        "nama": nama_komik
    }

    hasil.append(item)

    print()
    print("******** KOMIK DITEMUKAN ********")
    print("Mapel  :", mapel)
    print("Folder :", folder.as_posix())
    print("File   :", relative_path.as_posix())
    print("*********************************")
    print()

# ============================================================
# URUTKAN
# ============================================================

hasil.sort(
    key=lambda x: (
        x["mapel"].lower(),
        x["folder"].lower()
    )
)

# ============================================================
# BUAT JSON
# ============================================================

data = {
    "folder": ".",
    "total": len(hasil),
    "komik": hasil
}

# ============================================================
# SIMPAN
# ============================================================

OUTPUT.write_text(
    json.dumps(
        data,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)

# ============================================================
# HASIL
# ============================================================

print("=" * 70)
print("HASIL AKHIR")
print("=" * 70)

print("Total komik:", len(hasil))
print()

if hasil:

    for nomor, item in enumerate(hasil, start=1):

        print(
            f"{nomor}. "
            f"[{item['mapel']}] "
            f"{item['path']}"
        )

else:

    print(
        "TIDAK ADA halaman-00.jpg "
        "YANG DITEMUKAN."
    )

print()
print("File JSON:", OUTPUT)
print("=" * 70)
