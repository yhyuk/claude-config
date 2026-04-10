#!/usr/bin/env python3

import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple

class WeeklyTaskManager:
    def __init__(self):
        self.vault_path = Path(os.environ.get("OBSIDIAN_VAULT_PATH", Path.home() / "Documents" / "Obsidian Vault"))
        self.daily_path = self.vault_path / "00_HOME" / "daily"

    def get_current_week_file(self) -> Path:
        """현재 주차 파일 경로 반환"""
        today = datetime.now()
        year = today.strftime('%Y')
        month = today.strftime('%m')

        # 주차 계산 (월의 첫날부터 계산)
        first_day = today.replace(day=1)
        week_num = ((today - first_day).days // 7) + 1

        week_file = self.daily_path / year / month / f"{week_num}주차.md"
        week_file.parent.mkdir(parents=True, exist_ok=True)

        return week_file

    def parse_tasks(self, content: str) -> Dict[str, List[str]]:
        """마크다운 내용에서 작업 파싱"""
        tasks = {
            'done': [],
            'todo': [],
            'in_progress': []
        }

        lines = content.split('\n')
        current_section = None

        for line in lines:
            if '[DONE]' in line:
                current_section = 'done'
            elif '[TODO]' in line:
                current_section = 'todo'
            elif '- [x]' in line and current_section:
                tasks['done'].append(line.strip())
            elif '- [ ]' in line and current_section:
                tasks['todo'].append(line.strip())
            elif '- [~]' in line and current_section:
                tasks['in_progress'].append(line.strip())

        return tasks

    def add_task(self, task: str, project: str = "General", priority: str = "Normal"):
        """새 작업 추가"""
        week_file = self.get_current_week_file()

        # 파일이 없으면 템플릿 생성
        if not week_file.exists():
            self.create_week_template(week_file)

        content = week_file.read_text(encoding='utf-8')

        # TODO 섹션에 작업 추가
        today = datetime.now().strftime('%y.%m.%d')
        new_task = f"\t- [ ] [{priority}] {task} ({project})\n\t{today}"

        # TODO 섹션 찾아서 추가
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '[TODO]' in line:
                # 프로젝트 찾기
                project_found = False
                for j in range(i+1, len(lines)):
                    if lines[j].startswith(project):
                        # 프로젝트 아래에 추가
                        for k in range(j+1, len(lines)):
                            if not lines[k].startswith('\t') and lines[k].strip():
                                lines.insert(k, new_task)
                                project_found = True
                                break
                        break

                if not project_found:
                    # 새 프로젝트 섹션 생성
                    lines.insert(i+1, f"{project}\n{new_task}")
                break

        week_file.write_text('\n'.join(lines), encoding='utf-8')
        print(f"작업 추가됨: {task}")

    def mark_task_done(self, task_pattern: str):
        """작업을 완료로 표시"""
        week_file = self.get_current_week_file()
        if not week_file.exists():
            print("현재 주차 파일이 없습니다.")
            return

        content = week_file.read_text(encoding='utf-8')

        # 패턴 매칭으로 작업 찾기
        pattern = re.compile(r'- \[ \].*' + re.escape(task_pattern), re.IGNORECASE)
        updated_content = pattern.sub(lambda m: m.group().replace('- [ ]', '- [x]'), content)

        if content != updated_content:
            week_file.write_text(updated_content, encoding='utf-8')
            print(f"작업 완료 표시: {task_pattern}")

            # DONE 섹션으로 이동
            self.move_completed_tasks()
        else:
            print(f"작업을 찾을 수 없습니다: {task_pattern}")

    def move_completed_tasks(self):
        """완료된 작업을 DONE 섹션으로 이동"""
        week_file = self.get_current_week_file()
        if not week_file.exists():
            return

        content = week_file.read_text(encoding='utf-8')
        lines = content.split('\n')

        done_tasks = []
        new_lines = []
        in_todo = False

        for line in lines:
            if '[TODO]' in line:
                in_todo = True
            elif '[DONE]' in line:
                in_todo = False

            if in_todo and '- [x]' in line:
                done_tasks.append(line)
            else:
                new_lines.append(line)

        # DONE 섹션에 추가
        if done_tasks:
            for i, line in enumerate(new_lines):
                if '[DONE]' in line:
                    # 적절한 위치에 삽입
                    for task in done_tasks:
                        new_lines.insert(i+1, task)
                    break

            week_file.write_text('\n'.join(new_lines), encoding='utf-8')
            print(f"{len(done_tasks)}개 작업을 DONE으로 이동")

    def create_week_template(self, week_file: Path):
        """주간 템플릿 생성"""
        week_num = week_file.stem
        year_month = week_file.parent.name

        template = f"""[DONE]

[TODO]

[MEMO]

[확인 요청]

---
### Link
[[{week_file.parent.parent.name}-{year_month}]]
"""
        week_file.write_text(template, encoding='utf-8')
        print(f"주간 템플릿 생성: {week_file}")

    def generate_weekly_report(self) -> str:
        """주간 보고서 생성"""
        week_file = self.get_current_week_file()
        if not week_file.exists():
            return "현재 주차 파일이 없습니다."

        content = week_file.read_text(encoding='utf-8')
        tasks = self.parse_tasks(content)

        report = f"""# 주간 업무 보고서
## 기간: {week_file.stem}

### 완료된 작업 ({len(tasks['done'])}개)
{''.join(tasks['done'])}

### 진행 중인 작업 ({len(tasks['in_progress'])}개)
{''.join(tasks['in_progress'])}

### 예정된 작업 ({len(tasks['todo'])}개)
{''.join(tasks['todo'])}

### 완료율
{len(tasks['done']) / (len(tasks['done']) + len(tasks['todo']) + len(tasks['in_progress'])) * 100:.1f}% 완료
"""
        return report

if __name__ == "__main__":
    manager = WeeklyTaskManager()

    # 사용 예시
    # manager.add_task("API 문서 작성", "my-project", "High")
    # manager.mark_task_done("API 문서")
    # print(manager.generate_weekly_report())