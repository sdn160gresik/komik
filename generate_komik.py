
from pathlib import Path
from urllib.parse import quote
import json
import re


# =========================================================
# KONFIGURASI GENERATOR LITERASI
# UPT SDN 160 GRESIK - PETUALANGAN KELAS 5
# =========================================================

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "komik.json"

THUMBNAIL_NAME = "halaman-00.jpg"

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
}

# Urutan khusus untuk materi yang sudah ada.
# Materi baru otomatis diurutkan setelah materi khusus.
URUTAN_KHUSUS = {
    "ipas/DIMANA_INDONESIA_BERADA?": 1,
    "mtk/bab1_A-D": 2,
    "ipas/MAJULAH_DAERAHKU": 3,
}


# =========================================================
# FUNGSI PENDUKUNG
# =========================================================

def natural_key(value):
    """Mengurutkan nama file berdasarkan angka secara alami."""
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", str(value))
    ]


def is_excluded(relative_path):
    """Mengabaikan folder dan file sistem yang tidak diperlukan."""
    parts = Path(relative_path).parts

    excluded_directories = {
        ".git",
        ".github",
        "__pycache__",
        "node_modules",
    }

    for part in parts:
        if part in excluded_directories:
            return True

        # Abaikan direktori tersembunyi.
        if part.startswith("."):
            return True

    return False


# =========================================================
# GENERATOR DAFTAR KOMIK
# =========================================================

def main():
    comics = []

    # Cari seluruh thumbnail di dalam repositori.
    for thumbnail in ROOT.rglob("*"):

        if not thumbnail.is_file():
            continue

        relative_thumbnail = thumbnail.relative_to(ROOT)

        if is_excluded(relative_thumbnail):
            continue

        if thumbnail.name.lower() != THUMBNAIL_NAME.lower():
            continue

        folder_path = thumbnail.parent

        relative_folder = folder_path.relative_to(ROOT).as_posix()

        # Materi harus berada di dalam folder mata pelajaran.
        # Contoh: mtk/bab2 atau ipas/MAJULAH_DAERAHKU.
        parts = Path(relative_folder).parts

        if len(parts) < 2:
            print(
                f"Lewati folder tanpa mapel induk: "
                f"{relative_folder}"
            )
            continue

        # Ambil semua gambar halaman selain thumbnail.
        page_files = [
            file
            for file in folder_path.iterdir()
            if (
                file.is_file()
                and file.suffix.lower() in IMAGE_EXTENSIONS
                and file.name.lower() != THUMBNAIL_NAME.lower()
                and not is_excluded(
                    file.relative_to(ROOT)
                )
            )
        ]

        # Urutkan halaman: 1, 2, 3, ... 10.
        page_files.sort(key=lambda file: natural_key(file.name))

        pages = []

        for file in page_files:
            relative_path = file.relative_to(ROOT).as_posix()

            pages.append({
                "file": file.name,
                "path": relative_path,
            })

        thumbnail_path = relative_thumbnail.as_posix()

        # Buat URL gambar yang aman untuk nama folder
        # dengan spasi, tanda tanya, atau karakter khusus.
        thumbnail_url = (
            "https://raw.githubusercontent.com/"
            "sdn160gresik/komik/main/"
            + quote(thumbnail_path, safe="/")
        )

        comics.append({
            "urutan": URUTAN_KHUSUS.get(
                relative_folder, 9999
            ),
            "reader": "literasi.html",
            "mapel": parts[0],
            "folder": relative_folder,
            "path": thumbnail_path,
            "thumbnail_url": thumbnail_url,
            "file": thumbnail.name,
            "nama": folder_path.name,
            "total_halaman": len(pages),
            "pages": pages,
        })

    # Urutkan materi berdasarkan urutan khusus,
    # kemudian mata pelajaran dan nama folder.
    comics.sort(
        key=lambda item: (
            item["urutan"],
            item["mapel"].lower(),
            item["folder"].lower(),
        )
    )

    data = {
        "folder": ".",
        "total": len(comics),
        "komik": comics,
    }

    # Tulis ulang komik.json, termasuk jika ada materi
    # yang thumbnail-nya sudah dihapus dari repositori.
    OUTPUT.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print(
        f"Berhasil membuat {OUTPUT.name}: "
        f"{len(comics)} materi komik ditemukan."
    )

    for item in comics:
        print(
            f"- {item['folder']} "
            f"({item['total_halaman']} halaman)"
        )


if __name__ == "__main__":
    main()
