#!/bin/bash

# 옵시디언-클로드 코드 통합 실행 스크립트

OBSIDIAN_VAULT="/Users/imform-mm-2101/Documents/Obsidian Vault"
SCRIPTS_DIR="/Users/imform-mm-2101/.claude/scripts"

# 색상 설정
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 함수: 메뉴 표시
show_menu() {
    echo -e "${GREEN}=== 옵시디언-클로드 코드 통합 메뉴 ===${NC}"
    echo "1. 작업 추가"
    echo "2. 작업 완료 표시"
    echo "3. 주간 보고서 생성"
    echo "4. 개발 학습 노트 생성"
    echo "5. 클로드 세션 기록"
    echo "6. Git 동기화"
    echo "7. 오늘의 작업 요약"
    echo "0. 종료"
    echo -n "선택: "
}

# 함수: 작업 추가
add_task() {
    echo -n "작업 내용: "
    read task
    echo -n "프로젝트 (기본: General): "
    read project
    project=${project:-General}
    echo -n "우선순위 (High/Normal/Low): "
    read priority
    priority=${priority:-Normal}

    python3 <<EOF
import sys
sys.path.append('$SCRIPTS_DIR')
from weekly_task_manager import WeeklyTaskManager
manager = WeeklyTaskManager()
manager.add_task("$task", "$project", "$priority")
EOF
    echo -e "${GREEN}작업이 추가되었습니다!${NC}"
}

# 함수: 작업 완료 표시
complete_task() {
    echo -n "완료할 작업 패턴: "
    read pattern

    python3 <<EOF
import sys
sys.path.append('$SCRIPTS_DIR')
from weekly_task_manager import WeeklyTaskManager
manager = WeeklyTaskManager()
manager.mark_task_done("$pattern")
EOF
    echo -e "${GREEN}작업이 완료 처리되었습니다!${NC}"
}

# 함수: 주간 보고서 생성
generate_report() {
    python3 <<EOF
import sys
sys.path.append('$SCRIPTS_DIR')
from weekly_task_manager import WeeklyTaskManager
manager = WeeklyTaskManager()
print(manager.generate_weekly_report())
EOF
}

# 함수: 개발 학습 노트 생성
create_dev_note() {
    echo -n "주제: "
    read topic
    echo -n "카테고리 (Spring/React/Infra/Algorithm/ETC): "
    read category
    echo -n "학습 내용: "
    read content

    source "$SCRIPTS_DIR/obsidian_dev_note.sh"
    create_dev_note "$topic" "$category" "$content"
}

# 함수: 클로드 세션 기록
log_claude_session() {
    echo -n "세션 주제: "
    read topic
    echo -n "카테고리: "
    read category

    python3 <<EOF
import sys
sys.path.append('$SCRIPTS_DIR')
from claude_session_logger import ClaudeSessionLogger
logger = ClaudeSessionLogger()
session_content = {
    'question': input('질문/요청: '),
    'solution': input('해결 방법: '),
    'learnings': input('학습 포인트: '),
    'notes': input('추가 메모: ')
}
logger.log_session("$topic", session_content, "$category")
EOF
    echo -e "${GREEN}세션이 기록되었습니다!${NC}"
}

# 함수: Git 동기화
sync_git() {
    cd "$OBSIDIAN_VAULT"
    git add .
    git commit -m "vault backup: $(date +"%Y-%m-%d %H:%M:%S")"
    git pull --rebase
    git push
    echo -e "${GREEN}Git 동기화 완료!${NC}"
}

# 함수: 오늘의 작업 요약
daily_summary() {
    echo -e "${YELLOW}=== 오늘의 작업 요약 ===${NC}"

    # 오늘 수정된 파일 목록
    echo -e "\n${GREEN}오늘 수정된 노트:${NC}"
    find "$OBSIDIAN_VAULT" -name "*.md" -mtime -1 -type f | head -10

    # 주간 작업 현황
    echo -e "\n${GREEN}주간 작업 현황:${NC}"
    python3 <<EOF
import sys
sys.path.append('$SCRIPTS_DIR')
from weekly_task_manager import WeeklyTaskManager
manager = WeeklyTaskManager()
week_file = manager.get_current_week_file()
if week_file.exists():
    content = week_file.read_text(encoding='utf-8')
    tasks = manager.parse_tasks(content)
    print(f"✅ 완료: {len(tasks['done'])}개")
    print(f"🔄 진행중: {len(tasks['in_progress'])}개")
    print(f"📋 예정: {len(tasks['todo'])}개")
EOF
}

# 메인 루프
while true; do
    show_menu
    read choice

    case $choice in
        1) add_task ;;
        2) complete_task ;;
        3) generate_report ;;
        4) create_dev_note ;;
        5) log_claude_session ;;
        6) sync_git ;;
        7) daily_summary ;;
        0) echo "종료합니다."; break ;;
        *) echo -e "${RED}잘못된 선택입니다.${NC}" ;;
    esac

    echo -e "\n계속하려면 Enter를 누르세요..."
    read
    clear
done