#!/bin/bash

# ==========================================
# Claude Code Configuration - Install Script
# ==========================================
# 이 스크립트는 Claude Code 설정을 새로운 환경에 설치합니다.
#
# 사용법:
#   ./install.sh
#
# 작동 방식:
#   1. ~/.claude/ 디렉토리가 없으면 생성
#   2. 설정 파일들을 심볼릭 링크로 연결
#   3. 플러그인 설치 가이드 출력
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
echo -e "${BLUE}  Claude Code Configuration Installer${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ==========================================
# 1. ~/.claude/ 디렉토리 확인 및 생성
# ==========================================
echo -e "${YELLOW}[1/4] Checking ~/.claude/ directory...${NC}"
if [ ! -d "$CLAUDE_DIR" ]; then
    echo -e "  Creating $CLAUDE_DIR"
    mkdir -p "$CLAUDE_DIR"
    echo -e "  ${GREEN}✓ Created${NC}"
else
    echo -e "  ${GREEN}✓ Already exists${NC}"
fi
echo ""

# ==========================================
# 2. 기존 파일 백업 (심볼릭 링크가 아닌 경우)
# ==========================================
echo -e "${YELLOW}[2/4] Backing up existing files...${NC}"
BACKUP_DIR="$CLAUDE_DIR/backup-$(date +%Y%m%d-%H%M%S)"

backup_if_needed() {
    local file="$1"
    if [ -f "$file" ] && [ ! -L "$file" ]; then
        mkdir -p "$BACKUP_DIR"
        echo -e "  Backing up $(basename $file) → $BACKUP_DIR/"
        mv "$file" "$BACKUP_DIR/"
    fi
}

backup_if_needed "$CLAUDE_DIR/CLAUDE.md"
backup_if_needed "$CLAUDE_DIR/settings.json"
backup_if_needed "$CLAUDE_DIR/.omc-config.json"

if [ -d "$BACKUP_DIR" ]; then
    echo -e "  ${GREEN}✓ Backup created at: $BACKUP_DIR${NC}"
else
    echo -e "  ${GREEN}✓ No backup needed${NC}"
fi
echo ""

# ==========================================
# 3. 심볼릭 링크 생성
# ==========================================
echo -e "${YELLOW}[3/4] Creating symbolic links...${NC}"

create_symlink() {
    local src="$1"
    local dest="$2"

    # 기존 심볼릭 링크 제거
    if [ -L "$dest" ]; then
        rm "$dest"
    fi

    # 새 심볼릭 링크 생성
    ln -sf "$src" "$dest"
    echo -e "  ${GREEN}✓${NC} $(basename $dest) → $src"
}

create_symlink "$SCRIPT_DIR/config/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
create_symlink "$SCRIPT_DIR/config/settings.json" "$CLAUDE_DIR/settings.json"
create_symlink "$SCRIPT_DIR/config/.omc-config.json" "$CLAUDE_DIR/.omc-config.json"

# docs, scripts 디렉토리도 연결
if [ -d "$SCRIPT_DIR/docs" ]; then
    create_symlink "$SCRIPT_DIR/docs" "$CLAUDE_DIR/docs"
fi

if [ -d "$SCRIPT_DIR/scripts" ]; then
    create_symlink "$SCRIPT_DIR/scripts" "$CLAUDE_DIR/scripts"
fi

echo ""

# ==========================================
# 4. 플러그인 설치 안내
# ==========================================
echo -e "${YELLOW}[4/4] Plugin installation guide${NC}"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  필수 플러그인 설치${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Claude Code CLI를 실행한 후 다음 명령어를 실행하세요:"
echo ""
echo -e "${GREEN}# 1. Oh My Claude Code${NC}"
echo "   /oh-my-claudecode:omc-setup"
echo ""
echo -e "${GREEN}# 2. Everything Claude Code${NC}"
echo "   (OMC 설치 시 자동으로 설치됨)"
echo ""
echo -e "${GREEN}# 3. Claude HUD${NC}"
echo "   /claude-hud:setup"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ==========================================
# 완료
# ==========================================
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  Installation Complete! ✨${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "다음 단계:"
echo "  1. Claude Code CLI 실행"
echo "  2. 위의 플러그인 설치 명령어 실행"
echo "  3. 설정 확인: cat ~/.claude/CLAUDE.md"
echo ""

if [ -d "$BACKUP_DIR" ]; then
    echo -e "${YELLOW}⚠ 기존 설정 백업: $BACKUP_DIR${NC}"
    echo ""
fi
