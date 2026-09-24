#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "========================================"
echo " SAVE SERVER CHANGES"
echo "========================================"

if [ -z "$(git status --porcelain)" ]; then
    echo
    echo "✅ Tidak ada perubahan."
    exit 0
fi

echo
echo "=== PERUBAHAN SERVER ==="
git status --short

echo
echo "=== STAGE ==="
git add -A

echo
echo "=== YANG AKAN DI-COMMIT ==="
git diff --cached --name-status

echo
read -r -p "Commit dan push semua perubahan ini? [y/N] " CONFIRM

case "$CONFIRM" in
    y|Y|yes|YES)
        ;;
    *)
        echo "Dibatalkan."
        git restore --staged .
        exit 1
        ;;
esac

git commit -m "sync server changes $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main

echo
echo "✅ Perubahan server sudah masuk GitHub."
