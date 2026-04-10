# Claude Code Configuration

> Claude Code 설정을 여러 환경에서 동기화하기 위한 저장소

---

## 개요

이 저장소는 [Claude Code](https://docs.claude.com/claude-code)의 글로벌 설정, 플러그인 설정, 문서, 스크립트를 관리합니다. 심볼릭 링크를 사용하여 저장소와 `~/.claude/` 디렉토리를 연결하므로, 한 곳에서 수정하면 자동으로 양쪽에 반영됩니다.

### 포함된 내용
- 글로벌 설정 (`CLAUDE.md`, `settings.json`, `.omc-config.json`)
- 개발 가이드 문서 (`docs/`)
- 유틸리티 스크립트 (`scripts/`)
- 자동 설치/업데이트 스크립트

### 제외된 내용
- 런타임 데이터 (`history.jsonl`, `debug/`, `file-history/` 등)
- 플러그인 바이너리 (마켓플레이스에서 재설치)
- 프로젝트별 설정 (`projects/`)
- 민감 정보 (API 키, 토큰 등)

---

## 전제 조건

- [Claude Code CLI](https://docs.claude.com/claude-code) 설치
- Git
- Python 3 (Obsidian 연동 스크립트 사용 시)

---

## 빠른 시작

### 새 환경에 설치

```bash
# 1. 저장소 클론
git clone https://github.com/yhyuk/claude-config.git ~/workspace/claude-config

# 2. 설치 스크립트 실행
cd ~/workspace/claude-config
./install.sh

# 3. Claude Code CLI 실행 후 플러그인 설치 (아래 "플러그인 설치" 섹션 참고)
```

### 기존 설정을 저장소로 초기화

```bash
# 1. 저장소 디렉토리로 이동
cd ~/workspace/claude-config

# 2. Git 저장소 초기화
git init

# 3. 첫 커밋
git add .
git commit -m "feat: initial claude config"

# 4. 원격 저장소 연결
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

---

## 디렉토리 구조

```
claude-config/
├── .gitignore              # Git 제외 파일 목록
├── README.md               # 이 파일
├── install.sh              # 새 환경 설치 스크립트
├── update.sh               # 설정 업데이트 스크립트
│
├── config/                 # 핵심 설정 파일
│   ├── CLAUDE.md          # 글로벌 개발 가이드
│   ├── settings.json      # Claude Code 설정
│   └── .omc-config.json   # Oh My Claude Code 설정
│
├── docs/                   # 개발 문서
│   ├── project-structure.md
│   ├── tech-stack.md
│   ├── dev-setup.md
│   ├── code-style.md
│   ├── git-workflow.md
│   ├── testing-strategy.md
│   └── omc/               # Oh My Claude Code 가이드
│       ├── overview.md
│       ├── agent-catalog.md
│       ├── agents/
│       └── workflows/
│
└── scripts/                # 유틸리티 스크립트 (Obsidian 연동)
    ├── save_to_obsidian.py           # Obsidian 문서 저장 통합 스크립트
    ├── weekly_task_manager.py        # 주간 작업 관리
    ├── claude_session_logger.py      # Claude 세션 기록
    ├── obsidian_hook.py              # Claude Code hooks 연동
    ├── obsidian_dev_note.sh          # 개발 학습 노트 생성
    ├── obsidian_claude_integration.sh # 통합 메뉴 스크립트
    └── setup_obsidian_integration.sh  # Obsidian 연동 초기 설정
```

---

## 사용법

### install.sh

새 환경에 설정을 설치합니다.

```bash
cd ~/workspace/claude-config
./install.sh
```

동작:
1. `~/.claude/` 디렉토리 생성 (없을 경우)
2. 기존 설정 파일 백업 (심볼릭 링크가 아닌 경우)
3. `config/` 파일들을 `~/.claude/`에 심볼릭 링크
4. 플러그인 설치 가이드 출력

### update.sh

로컬에서 변경한 `~/.claude/` 설정을 저장소의 `config/`로 복사합니다.

```bash
cd ~/workspace/claude-config
./update.sh
```

동작:
1. `~/.claude/` 설정을 `config/`로 복사
2. `docs/`, `scripts/` 동기화 (있는 경우)
3. Git 변경 사항 확인 및 안내

### 설정 변경 후 저장소 업데이트

```bash
cd ~/workspace/claude-config
./update.sh
git diff
git add .
git commit -m "chore: update claude config"
git push
```

### 다른 환경에서 최신 설정 받기

```bash
cd ~/workspace/claude-config
git pull
# 심볼릭 링크가 자동으로 최신 파일을 반영하므로 추가 작업 불필요
```

---

## 동기화 워크플로우

```
환경 A                    GitHub                    환경 B
  |                        ^                         |
수정                    update.sh              git clone
  |                        |                         |
~/.claude/           git commit & push         install.sh
  |                        ^                         |
자동 반영            저장소 업데이트            심볼릭 링크
                           |                         |
                      git pull <------------- ~/.claude/
                                                     |
                                                 자동 반영
```

---

## 플러그인 설치

새 환경에서는 플러그인을 수동으로 설치해야 합니다.

Claude Code CLI를 실행한 후:

```bash
# 1. Oh My Claude Code (필수)
/oh-my-claudecode:omc-setup

# 2. Everything Claude Code
# (OMC 설치 시 자동으로 설치됨)

# 3. Claude HUD (선택)
/claude-hud:setup
```

플러그인 바이너리는 저장소에 포함되지 않으며, 각 환경에서 재설치해야 합니다.

---

## 보안 주의사항

### 안전하게 포함 가능
- 글로벌 개발 가이드
- 에디터 설정
- 플러그인 설정 (API 키 제외)
- 문서 및 스크립트

### 절대 커밋 금지
- API 키, 토큰
- 개인 정보
- 프로젝트별 민감 데이터
- `.env` 파일

### 권장사항
- `.gitignore` 수정 시 민감 정보 패턴이 제거되지 않도록 주의
- 커밋 전 `git diff`로 변경사항 확인

---

## 문제 해결

### 심볼릭 링크가 작동하지 않음
```bash
# 링크 상태 확인
ls -la ~/.claude/CLAUDE.md

# 링크 재생성
cd ~/workspace/claude-config
./install.sh
```

### 변경 사항이 반영되지 않음
```bash
# 심볼릭 링크 확인
readlink ~/.claude/CLAUDE.md
# 예상: <your-workspace>/claude-config/config/CLAUDE.md
```

### 플러그인이 작동하지 않음
```bash
# Claude Code CLI에서 플러그인 재설치
/oh-my-claudecode:omc-setup
```

---

## 환경변수

| 변수명 | 설명 | 기본값 |
|--------|------|--------|
| `OBSIDIAN_VAULT_PATH` | Obsidian 볼트 경로 | `$HOME/Documents/Obsidian Vault` |

Obsidian 연동 스크립트에서 사용됩니다. 볼트 경로가 기본값과 다른 경우 셸 설정 파일(`.zshrc`, `.bash_profile`)에 추가하세요:

```bash
export OBSIDIAN_VAULT_PATH="$HOME/path/to/your/vault"
```

---

## 관련 링크

- [Claude Code 공식 문서](https://docs.claude.com/claude-code)
- [Oh My Claude Code](https://github.com/cyanheads/oh-my-claudecode)
- [Everything Claude Code](https://github.com/cyanheads/everything-claude-code)

---

## 라이센스

MIT License
