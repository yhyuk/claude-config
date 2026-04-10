#!/usr/bin/env python3

"""
클로드 코드에서 직접 호출하여 옵시디언에 문서를 저장하는 통합 스크립트
프로젝트 위치와 무관하게 항상 옵시디언 볼트에 저장됨
"""

import os
import json
from datetime import datetime
from pathlib import Path
import re

class ObsidianDocManager:
    def __init__(self):
        self.vault_path = Path(os.environ.get("OBSIDIAN_VAULT_PATH", Path.home() / "Documents" / "Obsidian Vault"))
        self.learning_path = self.vault_path / "02_Learning"
        self.daily_path = self.vault_path / "00_HOME" / "daily"
        self.work_path = self.vault_path / "01_Work"

    def save_learning_note(self, title, content, category=None, tags=None, code_snippets=None):
        """
        학습 내용을 옵시디언에 저장

        Args:
            title: 문서 제목
            content: 문서 내용 (딕셔너리 또는 문자열)
            category: 카테고리 (Spring, React, Docker, Algorithm 등)
            tags: 태그 리스트
            code_snippets: 코드 예제 딕셔너리 {'language': 'code'}
        """
        # 카테고리 자동 감지
        if not category:
            category = self._detect_category(title, str(content))

        # 파일 경로 설정
        category_path = self.learning_path / category
        category_path.mkdir(parents=True, exist_ok=True)

        # 파일명 생성
        timestamp = datetime.now()
        safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
        filename = f"{timestamp.strftime('%Y-%m-%d')}_{safe_title}.md"
        filepath = category_path / filename

        # 마크다운 생성
        markdown = self._generate_markdown(title, content, category, tags, code_snippets, timestamp)

        # 파일 저장
        filepath.write_text(markdown, encoding='utf-8')

        # MOC 업데이트
        self._update_moc(category, filename, title)

        return str(filepath)

    def save_project_note(self, project_name, task_type, content):
        """
        프로젝트 관련 문서를 저장

        Args:
            project_name: 프로젝트명 (예: my-project)
            task_type: 작업 유형 (API문서, 이슈해결, 설계 등)
            content: 문서 내용
        """
        project_path = self.work_path / "Projects" / project_name
        project_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now()
        filename = f"{timestamp.strftime('%Y-%m-%d')}_{task_type}.md"
        filepath = project_path / filename

        markdown = f"""# {project_name} - {task_type}

## 날짜
{timestamp.strftime('%Y-%m-%d %H:%M')}

## 내용
{content if isinstance(content, str) else self._dict_to_markdown(content)}

---
[[_MOC_{project_name}]]
"""

        filepath.write_text(markdown, encoding='utf-8')
        return str(filepath)

    def update_weekly_task(self, task, status="todo", project="General"):
        """주간 작업 목록 업데이트"""
        today = datetime.now()
        year = today.strftime('%Y')
        month = today.strftime('%m')

        # 주차 계산
        first_day = today.replace(day=1)
        week_num = ((today - first_day).days // 7) + 1

        week_file = self.daily_path / year / month / f"{week_num}주차.md"

        if not week_file.exists():
            self._create_week_template(week_file)

        content = week_file.read_text(encoding='utf-8')

        # 작업 추가/업데이트 로직
        if status == "todo":
            marker = "- [ ]"
        elif status == "done":
            marker = "- [x]"
        else:
            marker = "- [~]"

        # TODO 섹션에 추가
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '[TODO]' in line and status == "todo":
                # 프로젝트 섹션 찾기 또는 생성
                task_line = f"\t{marker} {task}\n\t{today.strftime('%y.%m.%d')}"

                # 프로젝트 이름 아래에 추가
                project_idx = None
                for j in range(i+1, len(lines)):
                    if lines[j].strip() == project:
                        project_idx = j
                        break
                    elif lines[j].startswith('[') and ']' in lines[j]:
                        # 다른 섹션 시작
                        break

                if project_idx:
                    lines.insert(project_idx + 1, task_line)
                else:
                    # 프로젝트 섹션 생성
                    lines.insert(i + 1, f"{project}\n{task_line}")
                break

        week_file.write_text('\n'.join(lines), encoding='utf-8')
        return str(week_file)

    def save_session_summary(self, topic, problem, solution, learnings=None, code=None):
        """
        클로드 코드 세션 요약 저장
        간단한 인터페이스로 빠르게 저장
        """
        content = {
            'problem': problem,
            'solution': solution,
            'learnings': learnings or [],
            'code': code or {}
        }

        return self.save_learning_note(
            title=topic,
            content=content,
            category="Claude_Sessions",
            tags=['claude-code', 'session']
        )

    def _detect_category(self, title, content):
        """내용 기반으로 카테고리 자동 감지"""
        text = (title + " " + content).lower()

        categories = {
            'Spring': ['spring', 'boot', 'jpa', 'hibernate', '@autowired', '@service', '@repository'],
            'React': ['react', 'useState', 'useEffect', 'component', 'jsx', 'props'],
            'Docker': ['docker', 'container', 'dockerfile', 'docker-compose', 'kubernetes', 'k8s'],
            'Algorithm': ['algorithm', '알고리즘', 'sort', 'search', 'dp', 'graph', 'tree'],
            'Database': ['database', 'sql', 'query', 'table', 'index', 'mongodb', 'mysql'],
            'Infra': ['server', 'nginx', 'apache', 'aws', 'cloud', 'deploy', 'ci/cd'],
            'Java': ['java', 'class', 'interface', 'extends', 'implements'],
            'Python': ['python', 'def', 'import', 'pip', 'numpy', 'pandas'],
            'JavaScript': ['javascript', 'js', 'node', 'npm', 'var', 'let', 'const', 'function']
        }

        # 각 카테고리별 매칭 점수 계산
        scores = {}
        for cat, keywords in categories.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                scores[cat] = score

        # 가장 높은 점수의 카테고리 반환
        if scores:
            return max(scores, key=scores.get)

        return "ETC"

    def _generate_markdown(self, title, content, category, tags, code_snippets, timestamp):
        """마크다운 문서 생성"""
        # 태그 문자열 생성
        tag_str = ""
        if tags:
            tag_str = " ".join(f"#{tag}" for tag in tags)

        # 내용 처리
        if isinstance(content, dict):
            content_str = self._dict_to_markdown(content)
        else:
            content_str = content

        # 코드 스니펫 처리
        code_section = ""
        if code_snippets:
            code_section = "\n## 코드 예제\n"
            if isinstance(code_snippets, dict):
                for lang, code in code_snippets.items():
                    code_section += f"\n```{lang}\n{code}\n```\n"
            else:
                code_section += f"\n```\n{code_snippets}\n```\n"

        markdown = f"""# {title}

## 메타데이터
- **날짜**: {timestamp.strftime('%Y-%m-%d %H:%M')}
- **카테고리**: {category}
- **태그**: {tag_str}

## 내용
{content_str}

{code_section}

---
[[_MOC_{category}]]
"""
        return markdown

    def _dict_to_markdown(self, content_dict):
        """딕셔너리를 마크다운 형식으로 변환"""
        markdown = ""

        for key, value in content_dict.items():
            # 키를 제목으로 변환
            title = key.replace('_', ' ').title()

            if isinstance(value, list):
                markdown += f"\n### {title}\n"
                for item in value:
                    markdown += f"- {item}\n"
            elif isinstance(value, dict):
                markdown += f"\n### {title}\n"
                markdown += self._dict_to_markdown(value)
            else:
                markdown += f"\n### {title}\n{value}\n"

        return markdown

    def _update_moc(self, category, filename, title):
        """MOC 파일 업데이트"""
        moc_file = self.learning_path / category / f"_MOC_{category}.md"

        if not moc_file.exists():
            # MOC 파일 생성
            moc_content = f"""# {category} MOC

## 최근 문서
- [[{filename[:-3]}]] - {title}

## 카테고리별 정리
<!-- 자동으로 업데이트됨 -->
"""
            moc_file.write_text(moc_content, encoding='utf-8')
        else:
            # 기존 MOC에 추가
            content = moc_file.read_text(encoding='utf-8')
            lines = content.split('\n')

            # "최근 문서" 섹션 찾아서 추가
            for i, line in enumerate(lines):
                if '## 최근 문서' in line:
                    # 새 항목을 바로 아래에 추가
                    lines.insert(i + 1, f"- [[{filename[:-3]}]] - {title}")
                    break

            moc_file.write_text('\n'.join(lines), encoding='utf-8')

    def _create_week_template(self, week_file):
        """주간 템플릿 생성"""
        template = """[DONE]

[TODO]
General

[MEMO]

[확인 요청]

---
### Link
[[{parent}]]
""".format(parent=week_file.parent.name)

        week_file.parent.mkdir(parents=True, exist_ok=True)
        week_file.write_text(template, encoding='utf-8')

# 전역 인스턴스 생성
obsidian = ObsidianDocManager()

def save_to_obsidian(topic, content, **kwargs):
    """간단한 인터페이스로 옵시디언에 저장"""
    return obsidian.save_learning_note(topic, content, **kwargs)

def save_session(topic, problem, solution, **kwargs):
    """클로드 세션 저장"""
    return obsidian.save_session_summary(topic, problem, solution, **kwargs)

def save_project(project, task_type, content):
    """프로젝트 문서 저장"""
    return obsidian.save_project_note(project, task_type, content)

def add_task(task, project="General"):
    """주간 작업 추가"""
    return obsidian.update_weekly_task(task, "todo", project)

if __name__ == "__main__":
    print("옵시디언 문서 관리 시스템 준비 완료")