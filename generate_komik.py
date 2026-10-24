
import json
import re
from pathlib import Path
from urllib.parse import quote

# ============================================================
# KONFIGURASI
# ============================================================

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "komik.json"

EXCLUDE_DIRS = {
    ".git",
    ".github",
    "node_modules",
    "__pycache__",
}

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
}

THUMBNAIL_FILE = "halaman-00.jpg"

# Ganti jika nama akun atau repository berbeda.
GITHUB_USERNAME = "sdn160gresik"
GITHUB_REPO = "komik"
BRANCH = "main"

# Folder yang ingin ditampilkan lebih dahulu.
# Folder baru yang tidak dicantumkan akan diurutkan
# setelah folder yang memiliki urutan khusus.
PRIORITY_FOLDERS = {
    "ipas/DIMANA_INDONESIA_BERADA?": 1,
    "mtk/bab1_A-D": 2,
    "ipas/MAJULAH_DAERAHKU": 3,
}


# ============================================================
# FUNGSI URUTAN ALAMI
# halaman-2.jpg akan berada sebelum halaman-10.jpg.
# ============================================================

def natural_key(value):
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", value)
    ]


# ============================================================
# FUNGSI URL GITHUB
# ============================================================

def github_raw_url(relative_path):
    encoded_path = "/".join(
        quote(part, safe="")
        for part in Path(relative_path).parts
    )

    return (
        f"https://raw.githubusercontent.com/"
        f"{GITHUB_USERNAME}/{GITHUB_REPO}/"
        f"{BRANCH}/{encoded_path}"
    )


# ============================================================
# PEMERIKSAAN FOLDER
# ============================================================

print("=" * 70)
print("GENERATE DAFTAR LITERASI UPT SDN 160 GRESIK")
print("=" * 70)
print("Root       :", ROOT)
print("Output     :", OUTPUT)
print("Thumbnail  :", THUMBNAIL_FILE)
print()


# ============================================================
# CARI THUMBNAIL DAN HALAMAN DALAM FOLDER YANG SAMA
# ============================================================

komik = []

for thumbnail in ROOT.rglob("*"):

    if not thumbnail.is_file():
        continue

    relative_thumbnail = thumbnail.relative_to(ROOT)

    # Abaikan file di folder sistem.
    if any(
        part in EXCLUDE_DIRS
        for part in relative_thumbnail.parts
    ):
        continue

    # Hanya halaman-00.jpg yang menjadi thumbnail.
    if thumbnail.name.lower() != THUMBNAIL_FILE.lower():
        continue

    folder = thumbnail.parent
    folder_relative = folder.relative_to(ROOT)
    folder_string = folder_relative.as_posix()

    # Mapel ditentukan dari folder tingkat pertama.
    mapel = (
        folder_relative.parts[0]
        if len(folder_relative.parts) > 0
        else "lainnya"
    )

    # Nama materi diambil dari nama folder.
    nama = folder.name

    # Cari semua gambar dalam folder materi yang sama.
    semua_gambar = []

    for file in folder.iterdir():

        if not file.is_file():
            continue

        if file.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        semua_gambar.append(file)

    semua_gambar.sort(
        key=lambda file: natural_key(file.name)
    )

    # halaman-00.jpg hanya menjadi thumbnail.
    # File itu tidak dimasukkan ke urutan halaman pembaca.
    halaman_baca = [
        file for file in semua_gambar
        if file.name.lower() != THUMBNAIL_FILE.lower()
    ]

    # Data halaman berupa path relatif agar URL
    # dapat dibentuk secara konsisten oleh pembaca.
    pages = [
        {
            "file": file.name,
            "path": file.relative_to(ROOT).as_posix(),
        }
        for file in halaman_baca
    ]

    # Urutan khusus jika ditentukan.
    # Folder baru otomatis mendapatkan urutan terakhir.
    urutan = PRIORITY_FOLDERS.get(
        folder_string,
        9999
    )

    item = {
        "urutan": urutan,
        "mapel": mapel,
        "nama": nama,
        "folder": folder_string,
        "thumbnail": relative_thumbnail.as_posix(),
        "thumbnail_url": github_raw_url(
            relative_thumbnail.as_posix()
        ),
        "reader": "literasi-reader.html",
        "total_halaman": len(pages),
        "pages": pages,
    }

    komik.append(item)

    print("Materi ditemukan:", nama)
    print("  Mapel         :", mapel)
    print("  Folder        :", folder_string)
    print("  Thumbnail     :", relative_thumbnail.as_posix())
    print("  Jumlah halaman:", len(pages))
    print()


# ============================================================
# URUTKAN DAFTAR
# ============================================================

komik.sort(
    key=lambda item: (
        item["urutan"],
        item["mapel"].lower(),
        natural_key(item["nama"]),
        item["folder"].lower(),
    )
)

# ============================================================
# SIMPAN JSON
# ============================================================

data = {
    "folder": ".",
    "total": len(komik),
    "komik": komik,
}

OUTPUT.write_text(
    json.dumps(
        data,
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)

# ============================================================
# LAPORAN AKHIR
# ============================================================

print("=" * 70)
print("SELESAI")
print("=" * 70)
print("Total materi :", len(komik))
print("File JSON    :", OUTPUT)
print()

for nomor, item in enumerate(komik, start=1):
    print(
        f"{nomor}. {item['mapel']} | "
        f"{item['nama']} | "
        f"{item['total_halaman']} halaman | "
        f"{item['thumbnail']}"
    )

print("=" * 70)
