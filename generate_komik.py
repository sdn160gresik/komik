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
# URUTAN DAN READER KOMIK
# ============================================================

KOMIK_CONFIG = {
    "ipas/DIMANA_INDONESIA_BERADA?": {
        "urutan": 1,
        "reader": "literasi-1.html"
    },

    "mtk/bab1_A-D": {
        "urutan": 2,
        "reader": "literasi-2.html"
    },

    "ipas/MAJULAH_DAERAHKU": {
        "urutan": 3,
        "reader": "literasi-3.html"
    }
}


# ============================================================
# INFORMASI ROOT
# ============================================================

print("=" * 70)
print("GENERATE DAFTAR KOMIK")
print("=" * 70)

print("ROOT   :", ROOT)
print("TARGET :", TARGET_FILE)
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
                " -",
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

    if any(
        part in EXCLUDE_DIRS
        for part in file.parts
    ):
        continue

    relative_path = file.relative_to(ROOT)

    relative_string = relative_path.as_posix()


    # --------------------------------------------------------
    # TAMPILKAN FILE YANG BERADA DI MTK
    # --------------------------------------------------------

    if relative_string.lower().startswith("mtk/"):

        print(
            "FILE MTK:",
            relative_string
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

    folder_string = folder.as_posix()


    # --------------------------------------------------------
    # CEK KONFIGURASI KOMIK
    # --------------------------------------------------------

    config = KOMIK_CONFIG.get(
        folder_string
    )


    if config is None:

        print(
            "PERINGATAN:",
            "Folder belum memiliki konfigurasi:",
            folder_string
        )

        print(
            "Komik tetap dimasukkan dengan urutan terakhir."
        )

        urutan = 9999
        reader = ""

    else:

        urutan = config["urutan"]
        reader = config["reader"]


    # --------------------------------------------------------
    # BUAT ITEM
    # --------------------------------------------------------

    item = {

        "urutan": urutan,

        "reader": reader,

        "mapel": mapel,

        "folder": folder_string,

        "path": relative_string,

        "file": file.name,

        "nama": nama_komik

    }


    hasil.append(item)


    print()
    print("******** KOMIK DITEMUKAN ********")

    print(
        "Urutan :",
        urutan
    )

    print(
        "Reader :",
        reader
    )

    print(
        "Mapel  :",
        mapel
    )

    print(
        "Folder :",
        folder_string
    )

    print(
        "File   :",
        relative_string
    )

    print("*********************************")
    print()


# ============================================================
# URUTKAN BERDASARKAN URUTAN YANG DITENTUKAN
# ============================================================

hasil.sort(
    key=lambda x: x["urutan"]
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

print(
    "Total komik:",
    len(hasil)
)

print()


if hasil:

    for nomor, item in enumerate(
        hasil,
        start=1
    ):

        print(
            f"{nomor}. "
            f"[{item['urutan']}] "
            f"{item['mapel']} | "
            f"{item['folder']} | "
            f"{item['reader']}"
        )

else:

    print(
        "TIDAK ADA halaman-00.jpg "
        "YANG DITEMUKAN."
    )


print()

print(
    "File JSON:",
    OUTPUT
)

print("=" * 70)
