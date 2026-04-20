# CLAUDE.md - 프로젝트 가이드

> 이 프로젝트의 개발 가이드라인과 워크플로우입니다.
>
> **기본 전략**: everything-claude-code (ECC) 활용 + 프로젝트 특화 규칙

---

## 꼭 지킬것
- 이모지 사용 지양
- 다양한 플러그인을 사용하더라도 무조건 한국어로 응답해줄 것

## 프로젝트 핵심 문서

### 필수 참고 문서
프로젝트 시작 전 반드시 읽어야 할 문서들입니다.

1. **[프로젝트 구조](./docs/project-structure.md)** - 디렉토리 구조 및 파일 구성
   - 프론트엔드 구조
   - 백엔드 (Spring Boot) 구조
   - 모노레포 구조

2. **[기술 스택](./docs/tech-stack.md)** - 사용 기술 및 선택 이유
   - 언어, 프레임워크, 라이브러리
   - 의존성 관리 정책
   - 버전 관리 정책

3. **[개발 환경 설정](./docs/dev-setup.md)** - 로컬 환경 구축
   - 프론트엔드/백엔드 설정
   - 필수 도구 설치
   - 트러블슈팅

4. **[코드 스타일 가이드](./docs/code-style.md)** - 팀 코딩 컨벤션
   - TypeScript/JavaScript 스타일
   - Java/Spring Boot 스타일
   - 네이밍 규칙

5. **[Git 워크플로우](./docs/git-workflow.md)** - 브랜치 전략 및 커밋 규칙
   - Git Flow 전략
   - 커밋 메시지 규칙 (Conventional Commits)
   - PR/코드 리뷰 프로세스

6. **[테스트 전략](./docs/testing-strategy.md)** - 테스트 정책 및 커버리지
   - 테스트 피라미드
   - TDD 워크플로우
   - 커버리지 목표 (80%+)

---

## ECC (Everything Claude Code) 활용

### ECC란?
프로젝트 개발에 필요한 검증된 워크플로우, 에이전트, 도구를 제공하는 플러그인입니다.

### 주요 워크플로우

#### 계획 수립
```bash
# 일반 계획
/everything-claude-code:plan

# 합의 기반 계획 (복잡한 작업)
/oh-my-claudecode:ralplan

# 상세 계획 (고위험 작업)
/oh-my-claudecode:ralplan --deliberate
```

#### 개발 실행
```bash
# 자동 개발 (아이디어 → 코드)
/oh-my-claudecode:autopilot

# 완료까지 반복 실행
/oh-my-claudecode:ralph

# 팀 모드 (단계별 조율)
/oh-my-claudecode:team

# 병렬 처리
/oh-my-claudecode:ultrawork
```

#### 코드 품질
```bash
# 종합 코드 리뷰
/everything-claude-code:code-review

# 보안 리뷰
/everything-claude-code:security-review

# 빌드 수정
/everything-claude-code:build-fix

# 코드 단순화
Task(subagent_type: "oh-my-claudecode:code-simplifier", ...)
```

#### 테스트
```bash
# TDD 워크플로우
/everything-claude-code:tdd

# E2E 테스트 생성/실행
/everything-claude-code:e2e
```

#### 디버깅
```bash
# 버그 분석
/oh-my-claudecode:analyze

# 디버깅
Task(subagent_type: "oh-my-claudecode:debugger", ...)
```

---

## 빠른 참조

### 새로운 기능 개발 시

#### 1. 계획 단계
```bash
# 프로젝트 문서 확인
- 프로젝트 구조 확인
- 기술 스택 확인

# 계획 수립
/everything-claude-code:plan
```

#### 2. 개발 단계
```bash
# TDD로 개발
/everything-claude-code:tdd
"Implement [feature name]"

# 또는 일반 개발
/oh-my-claudecode:team
"Implement [feature name]"
```

#### 3. 검증 단계
```bash
# 코드 리뷰
/everything-claude-code:code-review

# 보안 검토 (인증/민감데이터 처리 시)
/everything-claude-code:security-review

# 테스트 실행 확인
npm test  # 또는 ./gradlew test
```

#### 4. 커밋
```bash
# Git 커밋 (컨벤션 준수)
git add .
git commit -m "feat: [feature description]"

# 또는 Claude에게 요청
"Create meaningful commits for this feature"
```

---

### 버그 수정 시

```bash
# 1. 분석
/oh-my-claudecode:analyze
"Debug [issue description]"

# 2. 수정
# ... 코드 수정 ...

# 3. 테스트
npm test

# 4. 커밋
git commit -m "fix: [bug description]"
```

---

### 리팩토링 시

```bash
# 1. 계획
/oh-my-claudecode:ralplan
"Refactor [component/module]"

# 2. 실행
/oh-my-claudecode:ralph
"Refactor following the plan"

# 3. 검증
# - 테스트 통과 확인
# - 기능 보존 확인
```

---

### 코드 리뷰 시

```bash
# 자동 리뷰 (병렬 실행)
/everything-claude-code:code-review
/everything-claude-code:security-review

# 체크리스트 (git-workflow.md 참조)
- [ ] 코드 스타일 준수
- [ ] 테스트 통과
- [ ] 보안 이슈 없음
- [ ] 커버리지 유지/향상
```

---

### 빌드 실패 시

```bash
# 빌드 에러 자동 수정
/everything-claude-code:build-fix

# 수정 후 검증
npm run build  # 또는 ./gradlew build
```

---

## 상황별 에이전트 선택

### 탐색/조사
```bash
Task(subagent_type: "oh-my-claudecode:explore",
     prompt: "Find [what you're looking for]",
     model: "haiku")
```

### 외부 문서 조회 (SDK/라이브러리)
```bash
# 반드시 구현 전에 공식 문서 확인!
Task(subagent_type: "oh-my-claudecode:document-specialist",
     prompt: "Look up [library] documentation")
```

### 아키텍처 설계
```bash
Task(subagent_type: "oh-my-claudecode:architect",
     prompt: "Review architecture for [system]",
     model: "opus")
```

### 일반 구현
```bash
Task(subagent_type: "oh-my-claudecode:executor",
     prompt: "Implement [feature]",
     model: "sonnet")
```

### 복잡한 구현
```bash
Task(subagent_type: "oh-my-claudecode:deep-executor",
     prompt: "Implement [complex feature]",
     model: "opus")
```

---

## 보안 가이드라인

### 인증/인가 구현 시
```bash
# 1. 구현
# ... 코드 작성 ...

# 2. 보안 리뷰 (필수!)
/everything-claude-code:security-review

# 3. 수정
# ... 보안 이슈 수정 ...
```

### 민감 정보 처리
- [금지] 절대 커밋 금지: `.env`, `credentials.json`, API keys
- [권장] 환경 변수 사용: `.env.example` 제공
- [권장] Secrets 관리: AWS Secrets Manager, Vault 등

---

## 테스트 정책

### 커버리지 목표
- **전체**: 80% 이상
- **핵심 비즈니스 로직**: 90% 이상
- **유틸리티**: 70% 이상

### TDD 워크플로우
```bash
# 새 기능은 TDD로
/everything-claude-code:tdd
"Implement [feature with tests]"
```

### 테스트 실행
```bash
# 단위 테스트
npm test  # 또는 ./gradlew test

# 커버리지
npm test -- --coverage
./gradlew jacocoTestReport

# E2E 테스트
npm run test:e2e
```

---

## Git 워크플로우 요약

### 브랜치 전략
```bash
main (production)
  ├── develop (개발 통합)
  │   ├── feature/user-auth
  │   ├── bugfix/login-error
  │   └── refactor/user-service
  └── hotfix/critical-bug
```

### 브랜치 생성
```bash
git checkout develop
git pull origin develop
git checkout -b feature/[feature-name]
```

### 커밋 규칙 (Conventional Commits)
```bash
feat: 새로운 기능
fix: 버그 수정
docs: 문서 변경
refactor: 리팩토링
test: 테스트 추가/수정
chore: 빌드, 설정 등

# 예시
git commit -m "feat: add user authentication"
git commit -m "fix: resolve login redirect issue"
```

### PR 생성
```bash
# GitHub CLI
gh pr create --title "feat: User authentication" \
  --body "Summary of changes..."

# 또는 Claude에게 요청
"Create PR for user authentication feature"
```

---

## 문제 해결

### 일반적인 문제

#### 빌드 실패
```bash
/everything-claude-code:build-fix
```

#### 테스트 실패
```bash
# 분석
/oh-my-claudecode:analyze
"Debug test failures"

# 수정 후 재실행
npm test
```

#### Git 충돌
```bash
# 분석 및 해결
Task(subagent_type: "oh-my-claudecode:debugger",
     prompt: "Analyze and resolve merge conflicts")
```

#### 의존성 문제
```bash
# 프론트엔드
rm -rf node_modules package-lock.json
npm install

# 백엔드
./gradlew clean build --refresh-dependencies
```

---

## 체크리스트

### 커밋 전
- [ ] 코드 스타일 준수 (`npm run lint`)
- [ ] 테스트 통과 (`npm test`)
- [ ] 빌드 성공 (`npm run build`)
- [ ] 불필요한 파일 제외 확인

### PR 생성 전
- [ ] 모든 변경사항 커밋
- [ ] 충돌 해결
- [ ] 코드 리뷰 (/everything-claude-code:code-review)
- [ ] 보안 검토 (필요 시)
- [ ] 테스트 커버리지 확인

### 배포 전
- [ ] 모든 테스트 통과
- [ ] 프로덕션 빌드 성공
- [ ] 환경 변수 설정 확인
- [ ] 보안 검토 완료
- [ ] 롤백 계획 수립

---

## 추가 리소스

### 프로젝트 문서
- [트러블슈팅 가이드](./docs/troubleshooting.md)
- [FAQ](./docs/faq.md)
- [용어 사전](./docs/glossary.md)

### 외부 리소스
- [ECC GitHub](https://github.com/cyanheads/everything-claude-code)
- [OMC Documentation](https://github.com/cyanheads/oh-my-claudecode)
- [Claude Code Docs](https://docs.claude.com/claude-code)

---

## 팁

### 효율적인 개발
1. **문서 먼저 확인** - 프로젝트 구조, 기술 스택 숙지
2. **SDK/API는 문서 조회 후 사용** - document-specialist 활용
3. **TDD 실천** - 테스트 먼저 작성
4. **작은 단위로 커밋** - 의미있는 커밋 메시지
5. **자주 푸시** - 작업 손실 방지

### ECC 활용 극대화
1. **자동화 우선** - 수동 작업보다 ECC 커맨드 활용
2. **병렬 실행** - 독립적인 작업은 병렬로
3. **검증 필수** - verifier, code-review 항상 실행
4. **문서 참조** - 불확실하면 document-specialist

---

## 도움말

### OMC/ECC 명령어
```bash
# 설정
/oh-my-claudecode:omc-setup
/everything-claude-code:setup

# 도움말
/oh-my-claudecode:omc-help

# 진단
/oh-my-claudecode:omc-doctor

# 취소
/oh-my-claudecode:cancel
```

### 학습 시스템
```bash
# 학습된 패턴 확인
/instinct-status

# 패턴 진화
/evolve

# 새 패턴 추출
/learn-eval
```

---

**마지막 업데이트**: 2026년 4월 20일
