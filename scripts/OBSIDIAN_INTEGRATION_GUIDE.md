# 옵시디언-클로드 코드 통합 가이드

## 설정 완료!

옵시디언과 클로드 코드를 연동하는 자동화 시스템이 설정되었습니다.

## 주요 기능

### 1. 개발 학습 노트 자동화

#### 클로드 세션 자동 기록
- 클로드 코드에서 작업한 내용이 자동으로 옵시디언에 저장됩니다
- 위치: `02_Learning/Claude_Sessions/`
- 코드 예제, 해결 과정, 학습 포인트가 구조화되어 저장됩니다

### 2. 주간 업무 관리 체계화

#### 현재 관리 방식
- `00_HOME/daily/2026/03/1주차.md` 형태로 관리
- [DONE], [TODO], [MEMO] 섹션으로 구분

#### 자동화 기능
- **작업 추가**: 프로젝트별, 우선순위별로 자동 분류
- **작업 완료**: 패턴 매칭으로 작업을 찾아 완료 처리
- **주간 보고서**: 완료율 통계와 함께 자동 생성
- **Git 동기화**: obsidian-git과 연동하여 자동 백업

## 사용 방법

### 방법 1: 터미널에서 통합 메뉴 사용
```bash
obsidian-claude
```

메뉴 옵션:
1. 작업 추가
2. 작업 완료 표시
3. 주간 보고서 생성
4. 개발 학습 노트 생성
5. 클로드 세션 기록
6. Git 동기화
7. 오늘의 작업 요약

### 방법 2: 클로드 코드에서 직접 사용
```bash
# 작업 추가
python3 /Users/imform-mm-2101/.claude/scripts/weekly_task_manager.py

# 세션 기록
python3 /Users/imform-mm-2101/.claude/scripts/claude_session_logger.py
```

### 방법 3: 클로드 커맨드 사용
클로드 코드에서 `/obsidian-task` 입력

## 활용 예시

### 개발 중 학습 내용 정리
1. 클로드 코드에서 문제 해결
2. 자동으로 세션 내용이 옵시디언에 저장
3. 나중에 검색하여 참고 가능

### 일일 작업 관리
1. 아침: `obsidian-claude`로 오늘의 작업 확인
2. 작업 중: 완료된 작업 실시간 체크
3. 퇴근 전: 주간 보고서 생성 및 Git 동기화

## 폴더 구조

```
Obsidian Vault/
├── 00_HOME/daily/2026/
│   └── 03/
│       ├── 1주차.md (주간 작업 관리)
│       └── 2026-03.md
├── 02_Learning/
│   └── Claude_Sessions/ (클로드 세션 자동 저장)
│       ├── 2026-03-05_session.md
│       └── _MOC_Claude_Sessions.md
└── CLAUDE.md (전역 설정)
```

## 추가 커스터마이징

### 프로젝트별 템플릿 추가
`weekly_task_manager.py`에서 프로젝트 리스트 수정:
- HMP-JP
- 병의원
- 강남언니
- 등...

### 학습 카테고리 확장
`claude_session_logger.py`에서 카테고리 추가:
- Spring
- React/Next.js
- Docker/K8s
- Algorithm
- 등...

## 문제 해결

### 권한 오류 발생 시
```bash
chmod +x /Users/imform-mm-2101/.claude/scripts/*.sh
chmod +x /Users/imform-mm-2101/.claude/scripts/*.py
```

### 별칭이 작동하지 않을 때
```bash
source ~/.zshrc
# 또는
source ~/.bash_profile
```

## 향후 개선 아이디어

1. **Slack 연동**: 작업 완료 시 Slack 알림
2. **통계 대시보드**: 주/월별 생산성 분석
3. **AI 요약**: 일일 학습 내용 자동 요약
4. **템플릿 확장**: 프로젝트별 커스텀 템플릿
5. **캘린더 뷰**: 옵시디언 캘린더 플러그인과 연동

## 지원

문제가 있거나 개선 사항이 있으면 언제든 클로드 코드에서 문의하세요!