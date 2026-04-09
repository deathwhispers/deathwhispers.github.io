#!/usr/bin/env bash
set -euo pipefail

MODE="quick"
SCOPE="changed"
STRICT_TAXONOMY="false"

for arg in "$@"; do
  case "$arg" in
    --full)
      MODE="full"
      ;;
    --all)
      SCOPE="all"
      ;;
    --strict-taxonomy)
      STRICT_TAXONOMY="true"
      ;;
    *)
      echo "未知参数: $arg" >&2
      exit 2
      ;;
  esac
done

collect_targets() {
  if [[ "$SCOPE" == "all" ]]; then
    find _posts -type f -name '*.md' | sort
    return
  fi

  {
    git diff --name-only --diff-filter=ACMR
    git diff --name-only --cached --diff-filter=ACMR
    git ls-files --others --exclude-standard

    if [[ "${GITHUB_ACTIONS:-}" == "true" ]]; then
      if [[ -n "${GITHUB_BASE_REF:-}" ]]; then
        git diff --name-only --diff-filter=ACMR "origin/${GITHUB_BASE_REF}...HEAD" || true
      elif git rev-parse --verify HEAD~1 >/dev/null 2>&1; then
        git diff --name-only --diff-filter=ACMR HEAD~1..HEAD || true
      fi
    fi
  } | awk '/^_posts\/.*\.md$/ {print}' | sort -u
}

TARGETS=()
while IFS= read -r line; do
  [[ -n "$line" ]] || continue
  TARGETS+=("$line")
done < <(collect_targets)

echo "[守门检查] 模式=${MODE} 范围=${SCOPE} 目标数=${#TARGETS[@]}"

echo "[守门检查] 编译 Python 脚本"
python3 -m py_compile scripts/*.py .github/scripts/*.py

if [[ ${#TARGETS[@]} -gt 0 ]]; then
  echo "[守门检查] 校验必填 YAML 字段"
  python3 scripts/check_frontmatter_required.py "${TARGETS[@]}"

  echo "[守门检查] 校验 Markdown 格式"
  python3 scripts/markdown_cleanup.py --check "${TARGETS[@]}"

  echo "[守门检查] 校验文章命名与日期"
  python3 scripts/check_post_filenames.py "${TARGETS[@]}"

  echo "[守门检查] 校验内部链接"
  python3 scripts/check_internal_links.py "${TARGETS[@]}" --root .
else
  echo "[守门检查] 未发现变更文章，跳过内容校验"
fi

if [[ "$STRICT_TAXONOMY" == "true" ]]; then
  echo "[守门检查] 严格检查标签/分类冲突"
  python3 scripts/check_taxonomy_collisions.py _posts
else
  echo "[守门检查] 跳过标签/分类冲突检查（加 --strict-taxonomy 开启）"
fi

if [[ "$MODE" == "full" ]]; then
  echo "[守门检查] 执行 Jekyll 构建"
  bundle exec jekyll b
fi

echo "[守门检查] 完成"
