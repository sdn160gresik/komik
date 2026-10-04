import json
from pathlib import Path

ROOT = Path("ipas")
OUTPUT = Path("komik.json")

hasil = []

if ROOT.exists():
    for file in ROOT.rglob("halaman-00.jpg"):
        if file.is_file():
            hasil.append({
                "folder": file.parent.as_posix(),
                "path": file.as_posix(),
                "file": file.name
            })

hasil.sort(key=lambda x: x["folder"].lower())

data = {
    "folder": "ipas",
    "total": len(hasil),
    "komik": hasil
}

OUTPUT.write_text(
    json.dumps(data, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("=" * 50)
print("UPDATE DAFTAR KOMIK")
print("=" * 50)
print("Folder:", ROOT)
print("Jumlah komik:", len(hasil))

for item in hasil:
    print("-", item["folder"])

print("=" * 50)
