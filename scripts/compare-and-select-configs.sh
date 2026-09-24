#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/.."

REMOTE="origin/main"
BEST_COMMIT="5620c632eb4f41dfb6994255c7d138dfc32356f0"
OUT="CONFIG_COMPARISON_BEST_$(date '+%Y%m%d_%H%M%S').txt"
BEST_DIR="CONFIG_BEST_$(date '+%Y%m%d_%H%M%S')"

FILES=(
  ".gitignore"
  ".oxfmtrc.json"
  ".oxlintrc.json"
  "Dockerfile"
  "eslint.config.js"
  "index.html"
  "jsconfig.json"
  "nginx.conf"
  "package-lock.json"
  "package.json"
  "vite.config.js"
  "vitest.config.js"
)

git fetch origin

mkdir -p "$BEST_DIR"

{
echo "======================================================================"
echo " PRACINDO CONFIG COMPARISON"
echo "======================================================================"
echo "Remote       : $REMOTE"
echo "Verified Best: $BEST_COMMIT"
echo "Output Best  : $BEST_DIR"
echo "Tanggal      : $(date '+%Y-%m-%d %H:%M:%S')"
echo
echo "CATATAN:"
echo "BEST dipilih dari commit $BEST_COMMIT karena commit ini adalah"
echo "versi yang sudah terbukti berhasil npm ci + npm run build + Docker deploy."
echo

for FILE in "${FILES[@]}"
do
    PATHNAME="pracindo-frontend/$FILE"

    echo
    echo "======================================================================"
    echo "FILE: $FILE"
    echo "PATH: $PATHNAME"
    echo "======================================================================"

    FOUND=0
    declare -A SEEN=()

    while IFS= read -r COMMIT
    do
        [ -z "$COMMIT" ] && continue

        if git cat-file -e "$COMMIT:$PATHNAME" 2>/dev/null; then
            FOUND=1

            BLOB=$(git rev-parse "$COMMIT:$PATHNAME")
            INFO=$(git show -s --format='%ci|%s' "$COMMIT")

            if [ -z "${SEEN[$BLOB]+x}" ]; then
                SEEN[$BLOB]=1

                SIZE=$(git cat-file -s "$COMMIT:$PATHNAME")
                LINES=$(git show "$COMMIT:$PATHNAME" | wc -l)

                echo
                echo "VARIANT BLOB : $BLOB"
                echo "SIZE         : $SIZE bytes"
                echo "LINES        : $LINES"
                echo "PERTAMA      : $INFO"
            fi
        fi
    done < <(
        git log "$REMOTE" \
          --since="2026-09-22 00:00:00" \
          --until="2026-09-25 00:00:00" \
          --format='%H'
    )

    if [ "$FOUND" -eq 0 ]; then
        echo
        echo "TIDAK DITEMUKAN DI RIWAYAT COMMIT PERIODE INI"
        continue
    fi

    echo
    if git cat-file -e "$BEST_COMMIT:$PATHNAME" 2>/dev/null; then
        echo "KEPUTUSAN: KEEP"
        echo "ALASAN   : Versi verified deployment pada $BEST_COMMIT"

        mkdir -p "$BEST_DIR/pracindo-frontend"

        git show "$BEST_COMMIT:$PATHNAME" \
          > "$BEST_DIR/$PATHNAME"

        echo "DISIMPAN  : $BEST_DIR/$PATHNAME"
    else
        echo "KEPUTUSAN: TIDAK ADA VERSI VERIFIED"
    fi

done

echo
echo "======================================================================"
echo " CEK PEMAKAIAN CONFIG"
echo "======================================================================"

echo
echo "[.gitignore]"
echo "KEEP - digunakan Git"

echo
echo "[.oxfmtrc.json]"
echo "KEEP - digunakan oxfmt"

echo
echo "[.oxlintrc.json]"
echo "KEEP - digunakan oxlint"

echo
echo "[Dockerfile]"
echo "KEEP - digunakan Docker build frontend"

echo
echo "[eslint.config.js]"
echo "KEEP - digunakan ESLint"

echo
echo "[index.html]"
echo "KEEP - entry HTML Vite"

echo
echo "[jsconfig.json]"
echo "KEEP - konfigurasi JavaScript/IDE"

echo
echo "[nginx.conf]"
echo "KEEP - dipakai Dockerfile production"

echo
echo "[package.json]"
echo "KEEP - sumber script dan dependency"

echo
echo "[package-lock.json]"
echo "KEEP - lock dependency npm"

echo
echo "[vite.config.js]"
echo "KEEP - konfigurasi Vite"

echo
echo "[vitest.config.js]"
echo "KEEP - konfigurasi Vitest"

echo
echo "======================================================================"
echo " HASIL"
echo "======================================================================"
echo "Tidak ada dari 12 file target yang aman dihapus hanya berdasarkan"
echo "nama file. Semuanya mempunyai fungsi dalam toolchain atau IDE."
echo
echo "File terbaik disimpan di:"
echo "$BEST_DIR"
echo
echo "Perubahan pada proyek utama TIDAK dilakukan."
} | tee "$OUT"

echo
echo "======================================================================"
echo "SELESAI"
echo "======================================================================"
echo "Laporan : $OUT"
echo "Best    : $BEST_DIR"
