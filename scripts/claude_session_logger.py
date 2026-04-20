#!/usr/bin/env python3

import os
import json
from datetime import datetime
from pathlib import Path

class ClaudeSessionLogger:
    def __init__(self):
        self.vault_path = Path(os.environ.get("OBSIDIAN_VAULT_PATH", Path.home() / "Documents" / "Obsidian Vault"))
        if not self.vault_path.exists():
            print(f"경고: Obsidian 볼트 경로가 존재하지 않습니다 ({self.vault_path})")
            print("OBSIDIAN_VAULT_PATH 환경변수를 설정하거나 볼트 경로를 확인하세요.")
        self.learning_path = self.vault_path / "02_Learning" / "Claude_Sessions"
        try:
            self.learning_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"디렉토리 생성 실패 ({self.learning_path}): {e}")

    def log_session(self, topic, content, category="ETC"):
        """클로드 코드 세션 내용을 옵시디언에 자동 저장"""
        today = datetime.now()
        filename = f"{today.strftime('%Y-%m-%d_%H%M')}_{topic.replace(' ', '_')}.md"
        filepath = self.learning_path / filename

        markdown_content = f"""# {topic}

## 세션 정보
- **날짜**: {today.strftime('%Y-%m-%d %H:%M')}
- **카테고리**: {category}

## 질문/요청
{content.get('question', '')}

## 해결 과정
{content.get('solution', '')}

## 코드 스니펫
```{content.get('language', 'python')}
{content.get('code', '')}
```

## 학습 포인트
{content.get('learnings', '')}

## 추가 메모
{content.get('notes', '')}

---
Tags: #claude-code #{category.lower()} #{topic.replace(' ', '-').lower()}
[[_MOC_Claude_Sessions]]
"""

        try:
            filepath.write_text(markdown_content, encoding='utf-8')
            print(f"세션 기록 저장: {filepath}")
        except OSError as e:
            print(f"세션 기록 저장 실패 ({filepath}): {e}")
            raise
        return filepath

    def create_moc(self):
        """Claude Sessions MOC 파일 생성"""
        moc_path = self.learning_path / "_MOC_Claude_Sessions.md"
        if not moc_path.exists():
            moc_content = """# Claude Code Sessions MOC

## 카테고리별 정리

### Spring
<!-- 자동으로 업데이트됨 -->

### React/Next.js
<!-- 자동으로 업데이트됨 -->

### Infrastructure
<!-- 자동으로 업데이트됨 -->

### Algorithm
<!-- 자동으로 업데이트됨 -->

### ETC
<!-- 자동으로 업데이트됨 -->

## 최근 세션
<!-- 자동으로 업데이트됨 -->
"""
            moc_path.write_text(moc_content, encoding='utf-8')
            print(f"MOC 파일 생성: {moc_path}")

if __name__ == "__main__":
    logger = ClaudeSessionLogger()
    logger.create_moc()

    # 사용 예시
    session_content = {
        'question': 'Spring Boot에서 비동기 처리 최적화 방법',
        'solution': 'ThreadPoolTaskExecutor 설정 및 @Async 어노테이션 활용',
        'code': '@EnableAsync\n@Configuration\npublic class AsyncConfig {...}',
        'language': 'java',
        'learnings': '- 스레드 풀 사이즈 계산법\n- 비동기 예외 처리 방법',
        'notes': '프로덕션 환경에서 모니터링 필수'
    }

    logger.log_session("Spring_비동기_처리", session_content, "Spring")