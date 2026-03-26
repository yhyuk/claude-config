# Claude Code Configuration

> 개인 Claude Code 설정을 여러 환경에서 동기화하기 위한 저장소

---

## 📚 개요

이 저장소는 Claude Code의 글로벌 설정, 플러그인 설정, 문서, 스크립트를 관리합니다. 심볼릭 링크를 사용하여 저장소와 `~/.claude/` 디렉토리를 연결하므로, 한 곳에서 수정하면 자동으로 양쪽에 반영됩니다.

### 포함된 내용
- ✅ 글로벌 설정 (`CLAUDE.md`, `settings.json`, `.omc-config.json`)
- ✅ 개발 가이드 문서 (`docs/`)
- ✅ 유용한 스크립트 (`scripts/`)
- ✅ 자동 설치/업데이트 스크립트

### 제외된 내용
- ❌ 런타임 데이터 (`history.jsonl`, `debug/`, `file-history/` 등)
- ❌ 플러그인 바이너리 (마켓플레이스에서 재설치)
- ❌ 프로젝트별 설정 (`projects/`)
- ❌ 민감 정보

---

## 🚀 빠른 시작

### 회사 PC (처음 설정)

```bash
# 1. 저장소 디렉토리로 이동
cd ~/workspace/claude-config

# 2. Git 저장소 초기화
git init

# 3. 첫 커밋
git add .
git commit -m "feat: initial claude config"

# 4. GitHub 저장소 연결 (본인의 저장소 URL로 변경)
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

### 집 PC (새 환경에 설치)

```bash
# 1. 저장소 클론
git clone <your-github-repo-url> ~/workspace/claude-config

# 2. 설치 스크립트 실행
cd ~/workspace/claude-config
./install.sh

# 3. Claude Code CLI 실행 후 플러그인 설치
# (install.sh가 안내한 명령어 실행)
```

---

## 📂 디렉토리 구조

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
│   └── testing-strategy.md
│
└── scripts/                # 유틸리티 스크립트
    └── ...
```

---

## 🔧 사용법

### 새 환경에 설치

```bash
# 저장소 클론
git clone <your-repo-url> ~/workspace/claude-config

# 설치 스크립트 실행
cd ~/workspace/claude-config
./install.sh
```

**install.sh 동작:**
1. `~/.claude/` 디렉토리 생성 (없을 경우)
2. 기존 설정 파일 백업 (심볼릭 링크가 아닌 경우)
3. `config/` 파일들을 `~/.claude/`에 심볼릭 링크
4. 플러그인 설치 가이드 출력

### 설정 변경 후 저장소 업데이트 (회사 PC → GitHub)

```bash
# 1. 업데이트 스크립트 실행
cd ~/workspace/claude-config
./update.sh

# 2. 변경 사항 확인
git diff

# 3. 커밋 & 푸시
git add .
git commit -m "chore: update claude config"
git push
```

**update.sh 동작:**
1. `~/.claude/` 설정을 `config/`로 복사
2. `docs/`, `scripts/` 동기화 (있는 경우)
3. Git 변경 사항 확인 및 안내

### 다른 환경에서 최신 설정 받기 (집 PC ← GitHub)

```bash
# 저장소로 이동
cd ~/workspace/claude-config

# 최신 변경사항 가져오기
git pull

# 심볼릭 링크가 자동으로 최신 파일을 가리킴
# 추가 작업 불필요!
```

---

## 🔄 워크플로우 예시

### 회사 PC에서 설정 수정
```bash
# 1. CLAUDE.md 수정
vi ~/.claude/CLAUDE.md

# 2. 저장소에 반영
cd ~/workspace/claude-config
./update.sh

# 3. Git 커밋 & 푸시
git add config/CLAUDE.md
git commit -m "docs: update development guide"
git push
```

### 집 PC에서 최신 설정 받기
```bash
# 1. 저장소 업데이트
cd ~/workspace/claude-config
git pull

# 2. 끝! (심볼릭 링크가 자동 반영)
```

---

## 🛠️ 플러그인 설치

새 환경에서는 플러그인을 수동으로 설치해야 합니다.

Claude Code CLI를 실행한 후:

```bash
# 1. Oh My Claude Code (필수)
/oh-my-claudecode:omc-setup

# 2. Everything Claude Code (자동 설치됨)
# (OMC 설치 시 자동)

# 3. Claude HUD (선택)
/claude-hud:setup
```

**참고**: 플러그인 바이너리는 저장소에 포함되지 않으며, 각 환경에서 재설치해야 합니다.

---

## 📋 체크리스트

### 처음 설정할 때 (회사 PC)
- [ ] `~/workspace/claude-config/` 디렉토리 생성 완료
- [ ] `git init` 실행
- [ ] GitHub Private 저장소 생성
- [ ] `git remote add origin <url>` 연결
- [ ] 첫 커밋 & 푸시 완료

### 새 환경에 설치할 때 (집 PC)
- [ ] `git clone` 완료
- [ ] `./install.sh` 실행
- [ ] Claude Code 플러그인 설치
- [ ] `cat ~/.claude/CLAUDE.md` 확인

### 설정 변경 후
- [ ] `./update.sh` 실행
- [ ] `git diff` 확인
- [ ] `git commit` & `git push`

---

## 🔐 보안 주의사항

### ✅ 안전하게 포함됨
- 글로벌 개발 가이드
- 에디터 설정
- 플러그인 설정 (API 키 제외)
- 문서 및 스크립트

### ❌ 절대 커밋 금지
- API 키, 토큰
- 개인 정보
- 프로젝트별 민감 데이터
- `.env` 파일

### 권장사항
- **Private 저장소 사용** (권장)
- `.gitignore` 수정 금지
- 커밋 전 `git diff` 확인

---

## 🆘 문제 해결

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

# 올바른 경로를 가리키는지 확인
# 예상: /Users/your-name/workspace/claude-config/config/CLAUDE.md
```

### 플러그인이 작동하지 않음
```bash
# 플러그인 재설치
# Claude Code CLI에서:
/oh-my-claudecode:omc-setup
```

### Git 충돌 발생
```bash
# 최신 변경사항 먼저 받기
git pull

# 충돌 해결 후
git add .
git commit
git push
```

---

## 📞 추가 정보

### 관련 문서
- [CLAUDE.md](./config/CLAUDE.md) - 글로벌 개발 가이드
- [Oh My Claude Code](https://github.com/cyanheads/oh-my-claudecode)
- [Everything Claude Code](https://github.com/cyanheads/everything-claude-code)
- [Claude Code Docs](https://docs.claude.com/claude-code)

### 스크립트 도움말
```bash
# install.sh - 새 환경 설치
./install.sh

# update.sh - 설정 업데이트
./update.sh
```

---

## 🔄 동기화 워크플로우 요약

```
회사 PC                   GitHub                    집 PC
  ↓                        ↑                         ↓
수정                    update.sh              git clone
  ↓                        ↓                         ↓
~/.claude/           git commit & push         install.sh
  ↓                        ↑                         ↓
자동 반영            저장소 업데이트            심볼릭 링크
                           ↓                         ↓
                      git pull ←─────────── ~/.claude/
                                                      ↓
                                                  자동 반영
```

---

**마지막 업데이트**: 2026-03-26
**라이센스**: Private (개인 사용)
