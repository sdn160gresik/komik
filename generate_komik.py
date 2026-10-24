from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent

def main():
    for thumbnail in ROOT.rglob("*"):
        # Lanjutkan kode yang sudah ada
        ...
def main():
    comics = []

    for thumbnail in ROOT.rglob("*"):
        if not thumbnail.is_file() or is_excluded(thumbnail.relative_to(ROOT)):
            continue
        if thumbnail.name.lower() != THUMBNAIL_NAME.lower():
            continue

        folder_path = thumbnail.parent
        relative_folder = folder_path.relative_to(ROOT).as_posix()

        # Folder materi harus berada di dalam folder mata pelajaran,
        # misalnya mtk/bab2 atau ipas/MAJULAH_DAERAHKU.
        parts = Path(relative_folder).parts
        if len(parts) < 2:
            print(f"Lewati folder tanpa mapel induk: {relative_folder}")
            continue

        page_files = [
            file for file in folder_path.iterdir()
            if file.is_file()
            and file.suffix.lower() in IMAGE_EXTENSIONS
            and file.name.lower() != THUMBNAIL_NAME.lower()
        ]
        page_files.sort(key=lambda file: natural_key(file.name))

        pages = []
        for file in page_files:
            relative_path = file.relative_to(ROOT).as_posix()
            pages.append({
                "file": file.name,
                "path": relative_path,
            })

        comics.append({
            "urutan": URUTAN_KHUSUS.get(relative_folder, 9999),
            "reader": "literasi.html",
            "mapel": parts[0],
            "folder": relative_folder,
            "path": thumbnail.relative_to(ROOT).as_posix(),
            "thumbnail_url": "https://raw.githubusercontent.com/sdn160gresik/komik/main/" + quote(thumbnail.relative_to(ROOT).as_posix(), safe="/"),
            "file": thumbnail.name,
            "nama": folder_path.name,
            "total_halaman": len(pages),
            "pages": pages,
        })

    comics.sort(key=lambda item: (
        item["urutan"],
        item["mapel"].lower(),
        item["folder"].lower(),
    ))

    data = {
        "folder": ".",
        "total": len(comics),
        "komik": comics,
    }
    OUTPUT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Berhasil membuat {OUTPUT.name}: {len(comics)} materi komik ditemukan.")
    for item in comics:
        print(f"- {item['folder']} ({item['total_halaman']} halaman)")


if __name__ == "__main__":
    main()
