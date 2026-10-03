import json
from pathlib import Path

root = Path("ipas")

hasil = [{"folder": f.parent.as_posix(), "path": f.as_posix(), "file": "halaman-00.jpg"} for f in root.rglob("halaman-00.jpg") if f.is_file()]

hasil.sort(key=lambda x: x["folder"].lower())

data = {"folder": "ipas", "total": len(hasil), "komik": hasil}

Path("komik.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

print("Jumlah komik:", len(hasil))
