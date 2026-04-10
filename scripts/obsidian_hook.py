#!/usr/bin/env python3

"""
클로드 코드 hooks 스크립트 - 옵시디언 자동 문서화
이 스크립트를 claude code settings의 hooks에 설정하여 사용
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# 경로 설정
VAULT_PATH = Path(os.environ.get("OBSIDIAN_VAULT_PATH", Path.home() / "Documents" / "Obsidian Vault"))
LEARNING_PATH = VAULT_PATH / "02_Learning" / "Claude_Sessions"
DAILY_PATH = VAULT_PATH / "00_HOME" / "daily"

def on_tool_call(tool_name, params):
    """툴 호출 시 자동 기록"""
    if tool_name in ['Edit', 'Write', 'Bash']:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'tool': tool_name,
            'params': params
        }

        # 일별 로그 파일에 추가
        today = datetime.now()
        log_file = LEARNING_PATH / f"{today.strftime('%Y-%m-%d')}_tools.jsonl"
        log_file.parent.mkdir(parents=True, exist_ok=True)

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

def on_session_end(session_summary):
    """세션 종료 시 요약 생성"""
    today = datetime.now()
    summary_file = LEARNING_PATH / f"{today.strftime('%Y-%m-%d_%H%M')}_session.md"

    content = f"""# Claude Code Session Summary

## 날짜
{today.strftime('%Y-%m-%d %H:%M')}

## 세션 요약
{session_summary.get('summary', 'N/A')}

## 주요 작업
{chr(10).join('- ' + task for task in session_summary.get('tasks', []))}

## 생성/수정 파일
{chr(10).join('- ' + file for file in session_summary.get('files', []))}

## 학습 포인트
{chr(10).join('- ' + point for point in session_summary.get('learnings', []))}

---
Tags: #claude-code #session
"""

    summary_file.write_text(content, encoding='utf-8')
    print(f"세션 요약 저장: {summary_file}")

def update_weekly_task(task_info):
    """주간 작업 목록 자동 업데이트"""
    today = datetime.now()
    year = today.strftime('%Y')
    month = today.strftime('%m')

    # 주차 계산
    first_day = today.replace(day=1)
    week_num = ((today - first_day).days // 7) + 1

    week_file = DAILY_PATH / year / month / f"{week_num}주차.md"

    if week_file.exists():
        content = week_file.read_text(encoding='utf-8')

        # 작업 상태에 따라 업데이트
        if task_info.get('status') == 'completed':
            # TODO -> DONE으로 이동
            content = content.replace(
                f"- [ ] {task_info['task']}",
                f"- [x] {task_info['task']}"
            )

        week_file.write_text(content, encoding='utf-8')

if __name__ == "__main__":
    # Hook 타입에 따라 실행
    hook_type = os.environ.get('CLAUDE_HOOK_TYPE', '')

    if hook_type == 'tool_call':
        on_tool_call(
            os.environ.get('TOOL_NAME'),
            json.loads(os.environ.get('TOOL_PARAMS', '{}'))
        )
    elif hook_type == 'session_end':
        on_session_end(json.loads(os.environ.get('SESSION_SUMMARY', '{}')))
    elif hook_type == 'task_update':
        update_weekly_task(json.loads(os.environ.get('TASK_INFO', '{}')))