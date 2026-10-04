import json
from pathlib import Path

# ============================================================
# KONFIGURASI
# ============================================================

ROOT = Path(".")
OUTPUT = Path("komik.json")

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

    # Pastikan benar-benar file
    if not file.is_file():
        continue

    # Lewati folder sistem
    if any(part in EXCLUDE_DIRS for part in file.parts):
        continue

    # Path relatif terhadap root repository
    relative_path = file.relative_to(ROOT)

    # Folder tempat halaman-00.jpg berada
    folder = relative_path.parent

    # Pastikan mempunyai folder induk
    if not folder.parts:
        continue

    # ========================================================
    # FOLDER PERTAMA = MAPEL
    # ========================================================

    mapel = folder.parts[0]

    # ========================================================
    # NAMA KOMIK
    # ========================================================

    nama_komik = folder.name

    # ========================================================
    # SIMPAN DATA
    # ========================================================

    hasil.append({
        "mapel": mapel,
        "folder": folder.as_posix(),
        "path": relative_path.as_posix(),
        "file": file.name,
        "nama": nama_komik
    })

# ============================================================
# URUTKAN DATA
# ============================================================

hasil.sort(
    key=lambda x: (
        x["mapel"].lower(),
        x["folder"].lower()
    )
)

# ============================================================
# DATA JSON
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
# TAMPILKAN HASIL
# ============================================================

print("=" * 60)
print("UPDATE DAFTAR KOMIK")
print("=" * 60)

print("Total komik:", len(hasil))
print()

for item in hasil:
    print(
        f"[{item['mapel']}] "
        f"{item['folder']} "
        f"-> {item['file']}"
    )

print()
print("=" * 60)
print("komik.json berhasil dibuat.")
print("=" * 60)
