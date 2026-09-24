#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "========================================"
echo " PRACINDO SAFE DEPLOY"
echo "========================================"

git fetch origin

if [ -n "$(git status --porcelain)" ]; then
    echo
    echo "❌ DEPLOY DIBATALKAN"
    echo "Masih ada perubahan lokal yang belum di-commit:"
    git status --short
    echo
    echo "Simpan perubahan terlebih dahulu:"
    echo "./scripts/save-server.sh"
    exit 1
fi

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
    echo
    echo "❌ DEPLOY DIBATALKAN"
    echo "Server belum sama dengan GitHub."
    echo
    echo "LOCAL : $LOCAL"
    echo "REMOTE: $REMOTE"
    echo
    echo "Jalankan:"
    echo "git pull --ff-only origin main"
    exit 1
fi

echo
echo "✅ Git bersih"
echo "✅ Server sama dengan GitHub"
echo

docker compose build frontend backend
docker compose up -d frontend backend

echo
echo "========================================"
echo " ✅ DEPLOY BERHASIL"
echo "========================================"

docker compose ps
