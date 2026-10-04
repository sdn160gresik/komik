import json
from pathlib import Path

# ============================================================
# KONFIGURASI
# ============================================================

ROOT = Path(".").resolve()
OUTPUT = ROOT / "komik.json"

# Folder yang tidak perlu diperiksa
EXCLUDE_DIRS = {
    ".git",
    ".github",
    "node_modules",
}

# Nama file yang dicari
TARGET_FILE = "halaman-00.jpg"

# ============================================================
# INFORMASI ROOT
# ============================================================

print("=" * 70)
print("GENERATE DAFTAR KOMIK")
print("=" * 70)
print("ROOT :", ROOT)
print("FILE :", TARGET_FILE)
print()

# ============================================================
# MENCARI FILE
# ============================================================

hasil = []

for file in ROOT.rglob("*"):

    # Harus file
    if not file.is_file():
        continue

    # Lewati folder yang tidak perlu
    if any(part in EXCLUDE_DIRS for part in file.parts):
        continue

    # --------------------------------------------------------
    # CASE-INSENSITIVE
    # halaman-00.jpg
    # HALAMAN-00.JPG
    # Halaman-00.jpg
    # semuanya dianggap sama
    # --------------------------------------------------------

    if file.name.lower() != TARGET_FILE.lower():
        continue

    # Path relatif terhadap repository
    relative_path = file.relative_to(ROOT)

    # Folder tempat file berada
    folder = relative_path.parent

    # Jangan proses jika file langsung berada di root
    if not folder.parts:
        continue

    # Folder paling atas = mapel
    mapel = folder.parts[0]

    # Folder tempat halaman-00.jpg berada
    nama_komik = folder.name

    item = {
        "mapel": mapel,
        "folder": folder.as_posix(),
        "path": relative_path.as_posix(),
        "file": file.name,
        "nama": nama_komik
    }

    hasil.append(item)

    print("DITEMUKAN:")
    print("  Mapel :", mapel)
    print("  Folder:", folder.as_posix())
    print("  File  :", relative_path.as_posix())
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
# BUAT DATA JSON
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
# HASIL AKHIR
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
    print("TIDAK ADA halaman-00.jpg YANG DITEMUKAN.")

print()
print("File dibuat:", OUTPUT)
print("=" * 70)
