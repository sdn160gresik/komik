#!/bin/bash

set -e

git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

git add komik.json

if git diff --cached --quiet; then
    echo "Tidak ada perubahan pada komik.json"
else
    git commit -m "Update daftar komik otomatis"
    git push
fi
