#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
用法：
  bash scripts/batch_note_intake.sh [目标路径] [--with-date] [--seed=<种子>]

示例：
  bash scripts/batch_note_intake.sh _posts
  bash scripts/batch_note_intake.sh _posts/personal/masterlearn --with-date --seed=notes-v1
EOF
}

TARGET="_posts"
MODE="no-date"
SEED="default"
TARGET_SET="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --with-date)
      MODE="with-date"
      ;;
    --seed=*)
      SEED="${1#*=}"
      ;;
    --*)
      echo "未知参数: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      if [[ "$TARGET_SET" == "false" ]]; then
        TARGET="$1"
        TARGET_SET="true"
      else
        echo "多余参数: $1" >&2
        usage >&2
        exit 2
      fi
      ;;
  esac
  shift
done

echo "[笔记接入] 目标=${TARGET} 模式=${MODE}"

python3 scripts/frontmatter_standardize.py "${TARGET}"
python3 scripts/markdown_cleanup.py "${TARGET}"

if [[ "${MODE}" == "with-date" ]]; then
  python3 scripts/redistribute_post_dates.py "${TARGET}" \
    --start 2021-09 \
    --end 2024-04 \
    --window-map scripts/config/date_windows.yml \
    --seed "${SEED}" \
    --apply
fi

python3 scripts/check_post_filenames.py "${TARGET}"
python3 scripts/check_taxonomy_collisions.py "${TARGET}"

echo "[笔记接入] 完成"
