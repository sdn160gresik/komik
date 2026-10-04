import json
from pathlib import Path

# ============================================================
# KONFIGURASI
# ============================================================

ROOT = Path(".")
OUTPUT = Path("komik.json")

# Folder utama yang dianggap sebagai mata pelajaran
MAPEL = {
    "ipas",
    "matematika",
    "bahasa-indonesia",
    "pancasila",
    "seni",
    "bahasa-jawa"
}

# Folder yang tidak perlu diperiksa
EXCLUDE_DIRS = {
    ".git",
    ".github",
    "node_modules"
}

# ============================================================
# MENCARI SEMUA halaman-00.jpg
# ============================================================

hasil = []

for file in ROOT.rglob("halaman-00.jpg"):

    # Harus berupa file
    if not file.is_file():
        continue

    # Lewati folder sistem
    if any(part in EXCLUDE_DIRS for part in file.parts):
        continue

    # Path relatif dari root repository
    relative_path = file.relative_to(ROOT)

    # Semua folder sebelum halaman-00.jpg
    folder = relative_path.parent

    # --------------------------------------------------------
    # Menentukan MAPEL
    # --------------------------------------------------------

    parts = folder.parts

    if not parts:
        continue

    mapel = parts[0].lower()

    # Hanya proses folder mata pelajaran
    if mapel not in MAPEL:
        continue

    # --------------------------------------------------------
    # Nama komik = folder tempat halaman-00.jpg berada
    # --------------------------------------------------------

    nama_komik = folder.name

    # --------------------------------------------------------
    # Simpan data
    # --------------------------------------------------------

    hasil.append({
        "mapel": mapel,
        "folder": folder.as_posix(),
        "path": relative_path.as_posix(),
        "file": file.name,
        "nama": nama_komik
    })

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
# SIMPAN komik.json
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
# INFORMASI HASIL
# ============================================================

print("=" * 60)
print("UPDATE DAFTAR KOMIK")
print("=" * 60)
print("Total komik:", len(hasil))
print()

for item in hasil:
    print(
        f"[{item['mapel']}] "
        f"{item['folder']}"
    )

print()
print("=" * 60)
print("komik.json berhasil dibuat.")
print("=" * 60)
