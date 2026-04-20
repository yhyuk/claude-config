# Autopilot 모드

> 아이디어부터 작동하는 코드까지 완전 자동 실행하는 워크플로우입니다.

## 목차
- [개요](#개요)
- [언제 사용하는가](#언제-사용하는가)
- [실행 파이프라인](#실행-파이프라인)
- [사용법](#사용법)
- [설정 옵션](#설정-옵션)
- [모범 사례](#모범-사례)
- [제한 사항](#제한-사항)

---

## 개요

**Autopilot**은 OMC의 완전 자동화 워크플로우로, 사용자의 요청을 받아 분석, 계획, 구현, 테스트, 검증까지 모든 과정을 자동으로 수행합니다.

### 핵심 특징
- [권장] **완전 자동화**: 사람 개입 없이 전체 프로세스 실행
- [권장] **다단계 파이프라인**: explore → analyst → planner → executor → test → verify → qa
- [권장] **자동 QA**: UltraQA 모드로 품질 보증
- [권장] **증거 기반 완료**: 모든 검증 통과해야 완료

### 주의사항
- [주의] 자동으로 코드 변경 발생
- [주의] 실행 전 현재 상태 커밋 권장
- [주의] 복잡한 작업은 시간 소요 가능
- [주의] 중간에 멈출 수 있음 (`/oh-my-claudecode:cancel`)

---

## 언제 사용하는가

### [권장] 적합한 경우

#### 1. 새로운 기능 개발
```bash
/oh-my-claudecode:autopilot
"Build a REST API for managing blog posts with CRUD operations"
```

#### 2. 프로토타입 빠른 구현
```bash
/oh-my-claudecode:autopilot
"Create a simple task management dashboard with React"
```

#### 3. 보일러플레이트 생성
```bash
/oh-my-claudecode:autopilot
"Set up authentication system with JWT and refresh tokens"
```

#### 4. 통합 작업
```bash
/oh-my-claudecode:autopilot
"Integrate Stripe payment processing"
```

---

### [금지] 부적합한 경우

#### 1. 탐색적 작업
```bash
# 나쁜 예
/oh-my-claudecode:autopilot
"Show me how the authentication works"

# 좋은 예
Task(subagent_type: "oh-my-claudecode:explore",
     prompt: "Find and explain authentication flow")
```

#### 2. 레거시 코드 대규모 리팩토링
```bash
# autopilot 대신
/oh-my-claudecode:ralplan --deliberate
"Refactor legacy authentication system"
# 그 후 ralph 사용
```

#### 3. 단순 버그 수정
```bash
# autopilot 대신
/oh-my-claudecode:analyze
"Debug login redirect issue"
```

---

## 실행 파이프라인

Autopilot은 다음 단계를 자동으로 실행합니다:

### 1단계: 탐색 (Explore)
**에이전트**: `explore` (haiku)

**수행 작업**:
- 프로젝트 구조 파악
- 관련 파일 찾기
- 기존 패턴 분석

```
입력: "Build user profile API"
출력: "Found existing user models, API routes structure, ..."
```

---

### 2단계: 분석 (Analyze)
**에이전트**: `analyst` (opus)

**수행 작업**:
- 요구사항 명확화
- 수용 기준 정의
- 기술적 고려사항 파악

```
입력: 탐색 결과 + 사용자 요청
출력: "Requirements: 1) GET /api/users/:id, 2) PUT /api/users/:id, ..."
```

---

### 3단계: 계획 (Plan)
**에이전트**: `planner` (opus)

**수행 작업**:
- 단계별 구현 계획
- 의존성 분석
- 리스크 평가

```
입력: 분석 결과
출력: "Step 1: Create DTO, Step 2: Implement service, ..."
```

---

### 4단계: 실행 (Execute)
**에이전트**: `executor` (sonnet) 또는 `deep-executor` (opus)

**수행 작업**:
- 계획에 따라 코드 구현
- 파일 생성/수정
- 의존성 추가

```
입력: 실행 계획
출력: "Created UserProfileDto.ts, Updated UserController.ts, ..."
```

---

### 5단계: 테스트 (Test)
**에이전트**: `test-engineer` (sonnet)

**수행 작업**:
- 단위 테스트 작성
- 통합 테스트 작성
- 테스트 실행

```
입력: 구현된 코드
출력: "Created UserController.test.ts, All 15 tests passing"
```

---

### 6단계: 검증 (Verify)
**에이전트**: `verifier` (sonnet/opus)

**수행 작업**:
- 모든 요구사항 충족 확인
- 테스트 통과 확인
- 빌드 성공 확인

```
입력: 완료된 구현
출력: "✓ All requirements met, ✓ Tests passing, ✓ Build successful"
```

---

### 7단계: QA (UltraQA)
**모드**: UltraQA 자동 활성화

**수행 작업**:
- 실제 동작 검증
- 엣지 케이스 테스트
- 실패 시 자동 수정 루프

```
실행: test → verify → fix → repeat (until success)
```

---

## 사용법

### 기본 사용

```bash
/oh-my-claudecode:autopilot
"Build a complete user authentication system with email/password"
```

### 상세 요청

```bash
/oh-my-claudecode:autopilot
"Implement REST API for task management:
- Create, read, update, delete tasks
- Filter by status and priority
- Pagination support
- Full test coverage
- TypeScript with Zod validation"
```

### 기존 코드 확장

```bash
/oh-my-claudecode:autopilot
"Add real-time notifications to the existing chat system using WebSockets"
```

---

## 설정 옵션

### 상태 확인

```bash
# 현재 autopilot 상태 확인
mcp__plugin_oh-my-claudecode_t__state_get_status(mode: "autopilot")
```

### 진행 중 취소

```bash
/oh-my-claudecode:cancel
```

### 상태 초기화

```bash
mcp__plugin_oh-my-claudecode_t__state_clear(mode: "autopilot")
```

---

## 실행 흐름 다이어그램

```
[사용자 요청]
     ↓
┌────────────────┐
│ 1. Explore     │ (haiku)  - 프로젝트 탐색
└────────┬───────┘
         ↓
┌────────────────┐
│ 2. Analyst     │ (opus)   - 요구사항 분석
└────────┬───────┘
         ↓
┌────────────────┐
│ 3. Planner     │ (opus)   - 실행 계획 수립
└────────┬───────┘
         ↓
┌────────────────┐
│ 4. Executor    │ (sonnet) - 코드 구현
└────────┬───────┘
         ↓
┌────────────────┐
│ 5. Test Eng    │ (sonnet) - 테스트 작성
└────────┬───────┘
         ↓
┌────────────────┐
│ 6. Verifier    │ (sonnet) - 검증
└────────┬───────┘
         ↓
     [성공?]
      ↙    ↘
    YES    NO → [UltraQA]
     ↓              ↓
  [완료]      [수정 루프]
                   ↓
              [재검증]
```

---

## 모범 사례

### 1. 명확한 목표 설정

```bash
# [금지] 나쁜 예 - 모호함
/oh-my-claudecode:autopilot
"사용자 기능 만들어줘"

# [권장] 좋은 예 - 명확함
/oh-my-claudecode:autopilot
"Implement user registration and login with:
- Email/password authentication
- Password hashing with bcrypt
- JWT token generation
- Input validation with Zod
- Unit and integration tests"
```

---

### 2. 실행 전 준비

```bash
# 1. 현재 작업 커밋
git add .
git commit -m "Before autopilot: clean state"

# 2. Autopilot 실행
/oh-my-claudecode:autopilot
"[your request]"

# 3. 결과 확인 후 커밋 또는 롤백
git diff  # 변경 사항 확인
git commit -m "feat: implemented by autopilot"
# 또는
git reset --hard HEAD  # 롤백
```

---

### 3. 단계별 검증

Autopilot이 각 단계를 완료할 때마다 확인:

```
✓ Explore 완료   → 올바른 파일들 찾았는지 확인
✓ Analyst 완료   → 요구사항이 정확한지 확인
✓ Planner 완료   → 계획이 적절한지 확인
✓ Executor 완료  → 코드가 올바르게 작성되었는지 확인
✓ Test 완료      → 테스트가 충분한지 확인
✓ Verify 완료    → 모든 검증 통과했는지 확인
```

---

### 4. 복잡한 작업은 분할

```bash
# [금지] 나쁜 예 - 너무 큰 작업
/oh-my-claudecode:autopilot
"Build complete e-commerce platform with payment, inventory, shipping"

# [권장] 좋은 예 - 분할
/oh-my-claudecode:autopilot
"Implement product catalog API"

# 완료 후
/oh-my-claudecode:autopilot
"Add shopping cart functionality"

# 완료 후
/oh-my-claudecode:autopilot
"Integrate payment processing"
```

---

### 5. 문서 우선 (SDK/라이브러리 사용 시)

```bash
# 1. 먼저 문서 조회
Task(subagent_type: "oh-my-claudecode:document-specialist",
     prompt: "Look up Prisma ORM latest documentation")

# 2. 그 다음 autopilot
/oh-my-claudecode:autopilot
"Set up database with Prisma ORM for user management"
```

---

## 실전 예제

### 예제 1: 새 API 엔드포인트

```bash
/oh-my-claudecode:autopilot
"Create REST API endpoint for managing blog posts:

Requirements:
- GET /api/posts - List all posts (with pagination)
- GET /api/posts/:id - Get single post
- POST /api/posts - Create new post
- PUT /api/posts/:id - Update post
- DELETE /api/posts/:id - Delete post

Tech:
- Express.js
- TypeScript
- Zod validation
- Prisma ORM
- Full test coverage"
```

**자동 실행**:
1. 기존 API 구조 탐색
2. 요구사항 분석 및 명확화
3. 단계별 구현 계획
4. DTO, Controller, Service, Repository 구현
5. 테스트 작성
6. 검증 및 QA

---

### 예제 2: 인증 시스템

```bash
/oh-my-claudecode:autopilot
"Implement JWT-based authentication:

Features:
- User registration with email validation
- Login with email/password
- Access token (15 min) and refresh token (7 days)
- Token refresh endpoint
- Password hashing with bcrypt
- Protected routes middleware

Requirements:
- TypeScript
- Zod validation
- Unit tests for all functions
- Integration tests for auth flow"
```

---

### 예제 3: 외부 API 통합

```bash
# 1. 문서 조회
Task(subagent_type: "oh-my-claudecode:document-specialist",
     prompt: "Look up SendGrid Email API documentation")

# 2. Autopilot 실행
/oh-my-claudecode:autopilot
"Integrate SendGrid for email notifications:
- Welcome email on user registration
- Password reset email
- Email verification
- Environment variable configuration
- Error handling and retry logic
- Unit tests with mocks"
```

---

## 문제 해결

### Autopilot이 멈췄을 때

```bash
# 1. 상태 확인
mcp__plugin_oh-my-claudecode_t__state_read(mode: "autopilot")

# 2. 에러 확인 후 수동 수정

# 3. Autopilot 재개 또는 취소
/oh-my-claudecode:cancel
```

---

### 결과가 기대와 다를 때

```bash
# 1. 변경사항 확인
git diff

# 2. 문제 파악 후 선택
# Option A: 롤백하고 더 명확한 요청으로 재시도
git reset --hard HEAD
/oh-my-claudecode:autopilot "[more specific request]"

# Option B: 수동으로 수정
Task(subagent_type: "oh-my-claudecode:executor",
     prompt: "Fix [specific issue]")
```

---

### 테스트 실패 시

Autopilot의 UltraQA가 자동으로 처리하지만, 실패가 반복되면:

```bash
# 1. 취소
/oh-my-claudecode:cancel

# 2. 수동으로 디버깅
/oh-my-claudecode:analyze
"Debug why tests are failing"

# 3. 수정
Task(subagent_type: "oh-my-claudecode:executor",
     prompt: "Fix test failures")
```

---

## 제한 사항

### 1. 컨텍스트 크기
- 매우 큰 프로젝트에서는 분할 필요
- 한 번에 너무 많은 파일 변경 어려움

### 2. 복잡도
- 너무 복잡한 작업은 실패할 수 있음
- 단계별로 나눠서 실행 권장

### 3. 외부 의존성
- 외부 서비스 설정은 수동 필요
- 환경 변수 설정 필요

### 4. 도메인 지식
- 특정 도메인 로직은 명확한 설명 필요
- 비즈니스 규칙은 상세히 제공

---

## 대안 워크플로우

### Ralph - 완료까지 반복 실행
```bash
/oh-my-claudecode:ralph
"[your request]"
```
- Autopilot보다 더 집요하게 완료까지 반복
- 검증 에이전트가 완료 확인할 때까지

### Team - 조율된 팀 작업
```bash
/oh-my-claudecode:team
"[your request]"
```
- 더 구조화된 스테이지별 실행
- 각 스테이지마다 검토 포인트

### Ultrawork - 최대 병렬 처리
```bash
/oh-my-claudecode:ultrawork
"[your request]"
```
- 독립적 작업들 병렬 실행
- 속도 최우선

---

## 체크리스트

### 실행 전
- [ ] Git 상태 깨끗한가? (커밋 완료)
- [ ] 요청이 명확한가?
- [ ] SDK/API 문서 조회했는가?
- [ ] 적절한 크기의 작업인가?

### 실행 중
- [ ] 각 단계 결과 확인
- [ ] 예상과 다르면 중단하고 수정

### 완료 후
- [ ] 모든 테스트 통과하는가?
- [ ] 빌드 성공하는가?
- [ ] 변경사항 검토했는가?
- [ ] 커밋 또는 롤백 결정

---

## 참고
- [Ralph 모드](./ralph.md) - 더 집요한 완료 루프
- [Team 모드](./team.md) - 구조화된 팀 워크플로우
- [UltraQA](./ultraqa.md) - QA 사이클링 상세
- [에이전트 선택 가이드](../agents/selection-guide.md)
