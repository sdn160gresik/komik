import json
from pathlib import Path

root = Path("ipas")

hasil = [
{
"folder": file.parent.as_posix(),
"path": file.as_posix(),
"file": "halaman-00.jpg"
}
for file in root.rglob("halaman-00.jpg")
if file.is_file()
]

hasil.sort(key=lambda x: x["folder"].lower())

data = {
"folder": "ipas",
"total": len(hasil),
"komik": hasil
}

with open("komik.json", "w", encoding="utf-8") as f:
json.dump(data, f, ensure_ascii=False, indent=2)

print("Jumlah komik:", len(hasil))
