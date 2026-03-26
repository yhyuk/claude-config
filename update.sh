#!/bin/bash

# ==========================================
# Claude Code Configuration - Update Script
# ==========================================
# 이 스크립트는 회사 PC에서 변경한 설정을 저장소에 반영합니다.
#
# 사용법:
#   ./update.sh
#
# 작동 방식:
#   1. ~/.claude/ 의 설정 파일들을 config/ 로 복사
#   2. 변경 사항 확인 (git diff)
#   3. git add 준비 완료
# ==========================================

set -e  # 에러 발생 시 즉시 중단

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 현재 스크립트 디렉토리
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Claude Code Configuration Updater${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ==========================================
# 1. ~/.claude/ 디렉토리 확인
# ==========================================
echo -e "${YELLOW}[1/3] Checking ~/.claude/ directory...${NC}"
if [ ! -d "$CLAUDE_DIR" ]; then
    echo -e "${RED}✗ Error: ~/.claude/ directory not found${NC}"
    echo "Please run install.sh first."
    exit 1
fi
echo -e "  ${GREEN}✓ Found${NC}"
echo ""

# ==========================================
# 2. 설정 파일 복사
# ==========================================
echo -e "${YELLOW}[2/3] Copying configuration files...${NC}"

copy_if_exists() {
    local src="$1"
    local dest="$2"

    if [ -f "$src" ]; then
        # 심볼릭 링크인 경우 원본 파일 복사
        if [ -L "$src" ]; then
            src=$(readlink "$src")
        fi

        cp "$src" "$dest"
        echo -e "  ${GREEN}✓${NC} Copied $(basename $src)"
    else
        echo -e "  ${YELLOW}⚠${NC} Skipped $(basename $src) (not found)"
    fi
}

copy_if_exists "$CLAUDE_DIR/CLAUDE.md" "$SCRIPT_DIR/config/CLAUDE.md"
copy_if_exists "$CLAUDE_DIR/settings.json" "$SCRIPT_DIR/config/settings.json"
copy_if_exists "$CLAUDE_DIR/.omc-config.json" "$SCRIPT_DIR/config/.omc-config.json"

# docs, scripts 디렉토리도 동기화
if [ -d "$CLAUDE_DIR/docs" ]; then
    echo -e "  ${BLUE}Syncing docs directory...${NC}"
    rsync -av --delete "$CLAUDE_DIR/docs/" "$SCRIPT_DIR/docs/" > /dev/null
    echo -e "  ${GREEN}✓${NC} Synced docs/"
fi

if [ -d "$CLAUDE_DIR/scripts" ]; then
    echo -e "  ${BLUE}Syncing scripts directory...${NC}"
    rsync -av --delete "$CLAUDE_DIR/scripts/" "$SCRIPT_DIR/scripts/" > /dev/null
    echo -e "  ${GREEN}✓${NC} Synced scripts/"
fi

echo ""

# ==========================================
# 3. 변경 사항 확인
# ==========================================
echo -e "${YELLOW}[3/3] Checking for changes...${NC}"
echo ""

cd "$SCRIPT_DIR"

# Git 상태 확인
if git rev-parse --git-dir > /dev/null 2>&1; then
    if git diff --quiet && git diff --cached --quiet; then
        echo -e "${GREEN}No changes detected.${NC}"
    else
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${BLUE}  Changes Detected${NC}"
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        git status --short
        echo ""
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        echo "다음 명령어로 변경 사항을 확인하세요:"
        echo -e "  ${GREEN}git diff${NC}"
        echo ""
        echo "변경 사항을 커밋하려면:"
        echo -e "  ${GREEN}git add .${NC}"
        echo -e "  ${GREEN}git commit -m \"chore: update claude config\"${NC}"
        echo -e "  ${GREEN}git push${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Not a git repository. Initialize with:${NC}"
    echo "  git init"
    echo "  git add ."
    echo "  git commit -m \"feat: initial claude config\""
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  Update Complete! ✨${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
