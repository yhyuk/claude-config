#!/bin/bash

# 옵시디언-클로드 코드 통합 설정 스크립트

echo "=== 옵시디언-클로드 코드 통합 설정 ==="

# 1. 실행 권한 부여
chmod +x /Users/imform-mm-2101/.claude/scripts/*.sh
chmod +x /Users/imform-mm-2101/.claude/scripts/*.py

echo "✅ 스크립트 실행 권한 설정 완료"

# 2. 별칭 설정 (~/.zshrc 또는 ~/.bash_profile)
SHELL_CONFIG="$HOME/.zshrc"
if [ ! -f "$SHELL_CONFIG" ]; then
    SHELL_CONFIG="$HOME/.bash_profile"
fi

# 별칭이 이미 있는지 확인
if ! grep -q "alias obsidian-claude" "$SHELL_CONFIG"; then
    echo "" >> "$SHELL_CONFIG"
    echo "# 옵시디언-클로드 코드 통합" >> "$SHELL_CONFIG"
    echo "alias obsidian-claude='/Users/imform-mm-2101/.claude/scripts/obsidian_claude_integration.sh'" >> "$SHELL_CONFIG"
    echo "alias obs-task='python3 /Users/imform-mm-2101/.claude/scripts/weekly_task_manager.py'" >> "$SHELL_CONFIG"
    echo "alias obs-log='python3 /Users/imform-mm-2101/.claude/scripts/claude_session_logger.py'" >> "$SHELL_CONFIG"
    echo "✅ Shell 별칭 설정 완료"
else
    echo "ℹ️ Shell 별칭이 이미 설정되어 있습니다"
fi

# 3. Python 패키지 확인
echo ""
echo "Python 패키지 확인 중..."
python3 -c "from pathlib import Path; from datetime import datetime" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ 필요한 Python 패키지가 모두 설치되어 있습니다"
else
    echo "❌ Python 패키지 설치가 필요합니다"
fi

# 4. 옵시디언 볼트 확인
VAULT_PATH="/Users/imform-mm-2101/Documents/Obsidian Vault"
if [ -d "$VAULT_PATH" ]; then
    echo "✅ 옵시디언 볼트 확인 완료: $VAULT_PATH"
else
    echo "❌ 옵시디언 볼트를 찾을 수 없습니다: $VAULT_PATH"
fi

# 5. Claude Sessions 폴더 생성
SESSIONS_PATH="$VAULT_PATH/02_Learning/Claude_Sessions"
mkdir -p "$SESSIONS_PATH"
echo "✅ Claude Sessions 폴더 생성/확인 완료"

# 6. 사용법 안내
echo ""
echo "=== 설정 완료 ==="
echo ""
echo "사용 방법:"
echo "1. 터미널에서 'obsidian-claude' 실행하여 통합 메뉴 사용"
echo "2. 클로드 코드에서 '/obsidian-task' 커맨드 사용"
echo "3. Python 스크립트 직접 실행:"
echo "   - obs-task: 주간 작업 관리"
echo "   - obs-log: 클로드 세션 기록"
echo ""
echo "새 터미널을 열거나 'source $SHELL_CONFIG'를 실행하여 설정을 적용하세요."