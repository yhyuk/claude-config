# 에이전트 선택 가이드

> 상황별로 가장 적절한 에이전트를 선택하는 실용 가이드입니다.

## 목차
- [빠른 선택 테이블](#빠른-선택-테이블)
- [상황별 가이드](#상황별-가이드)
- [워크플로우별 추천](#워크플로우별-추천)
- [실전 예제](#실전-예제)
- [일반적인 실수](#일반적인-실수)

---

## 빠른 선택 테이블

| 상황 | 추천 에이전트 | 모델 | 대안 |
|-----|-------------|------|-----|
| 파일/코드 찾기 | explore | haiku | - |
| 요구사항 불명확 | analyst | opus | planner |
| 구현 계획 수립 | planner | opus | analyst → planner |
| 아키텍처 설계 | architect | opus | - |
| 단순 기능 구현 | executor | sonnet | - |
| 복잡한 기능 구현 | deep-executor | opus | executor |
| 버그 디버깅 | debugger | sonnet | - |
| 빌드/타입 에러 | build-fixer | sonnet | debugger |
| 종합 코드 리뷰 | code-reviewer | opus | quality-reviewer |
| 보안 검토 | security-reviewer | sonnet | code-reviewer |
| 품질 개선 | quality-reviewer | sonnet | code-reviewer |
| 테스트 작성 | test-engineer | sonnet | executor |
| 완료 검증 | verifier | sonnet | - |
| 문서 작성 | writer | haiku | - |
| 외부 문서 조회 | document-specialist | sonnet | - |
| 데이터 분석 | scientist | sonnet | - |

---

## 상황별 가이드

### 1. 새로운 기능 개발

#### 시나리오: "사용자 프로필 업데이트 API 만들기"

**단계별 에이전트 선택**:

```
1. 요구사항이 불명확한가?
   예 → analyst (opus)
   아니오 → 2번으로

2. 복잡도 평가
   간단 (1-2 파일) → executor (sonnet)
   중간 (3-5 파일) → planner (opus) → executor (sonnet)
   복잡 (5+ 파일, 여러 시스템) → planner (opus) → team

3. 구현
   executor (sonnet) 또는 deep-executor (opus)

4. 테스트
   test-engineer (sonnet)

5. 리뷰
   code-reviewer (opus)

6. 검증
   verifier (sonnet)
```

**실제 사용**:
```bash
# 간단한 경우
/oh-my-claudecode:team
"Implement user profile update API"

# 복잡한 경우
/oh-my-claudecode:autopilot
"Implement complete user management system"
```

---

### 2. 버그 수정

#### 시나리오: "로그인 후 리디렉션이 작동하지 않음"

**선택 흐름**:

```
1. 원인을 알고 있는가?
   예 → executor (sonnet) 직접 수정
   아니오 → debugger (sonnet)

2. debugger 결과
   → 원인 파악 완료
   → executor (sonnet) 수정

3. 테스트
   → 수동 테스트 또는 test-engineer

4. 검증
   → verifier (sonnet)
```

**실제 사용**:
```bash
# 원인 모름
/oh-my-claudecode:analyze
"Debug login redirect issue"

# 이후 수정
Task(
  subagent_type: "oh-my-claudecode:executor",
  prompt: "Fix redirect logic in AuthController based on debugger findings"
)
```

---

### 3. 리팩토링

#### 시나리오: "UserService의 중복 코드 제거"

**선택 흐름**:

```
1. 범위 파악
   explore (haiku) → 관련 파일 모두 찾기

2. 영향도 평가
   architect (opus) → 리팩토링 전략 리뷰

3. 계획 수립
   planner (opus) → 단계별 계획

4. 실행
   executor (sonnet) 또는 code-simplifier (opus)

5. 테스트
   test-engineer (sonnet) → 기존 테스트 유지/추가

6. 검증
   verifier (opus) → 기능 보존 확인
```

**실제 사용**:
```bash
# 전체 자동화
/oh-my-claudecode:ralph
"Refactor UserService to eliminate code duplication while maintaining all functionality"
```

---

### 4. 코드 리뷰

#### 시나리오: "PR 리뷰 필요"

**선택 기준**:

| PR 크기 | 변경 유형 | 추천 에이전트 |
|--------|----------|-------------|
| 소규모 (1-5 파일) | 일반 | quality-reviewer (sonnet) |
| 중규모 (6-15 파일) | 일반 | code-reviewer (opus) |
| 대규모 (15+ 파일) | 일반 | code-reviewer (opus) |
| 모든 크기 | 보안 관련 | security-reviewer (sonnet) |
| 모든 크기 | 성능 관련 | quality-reviewer (sonnet) |
| 모든 크기 | 아키텍처 변경 | architect (opus) |

**실제 사용**:
```bash
# 일반 리뷰
/oh-my-claudecode:code-review

# 보안 리뷰
/oh-my-claudecode:security-review

# 병렬 실행 (권장)
Task(subagent_type: "oh-my-claudecode:code-reviewer", ...)
Task(subagent_type: "oh-my-claudecode:security-reviewer", ...)
```

---

### 5. 빌드 실패

#### 시나리오: "TypeScript 타입 에러 100개"

**선택 흐름**:

```
1. 에러 유형 확인
   타입/빌드 에러 → build-fixer (sonnet)
   런타임/로직 에러 → debugger (sonnet)

2. build-fixer 실행
   → 최소 변경으로 빌드 복구

3. 추가 정리 필요시
   → quality-reviewer (sonnet)
   → code-simplifier (opus)
```

**실제 사용**:
```bash
# 빌드 수정
/oh-my-claudecode:build-fix

# 빌드 후 품질 개선
Task(
  subagent_type: "oh-my-claudecode:quality-reviewer",
  prompt: "Review and improve code quality after build fix"
)
```

---

### 6. 테스트 작성

#### 시나리오: "인증 모듈 테스트 필요"

**선택 기준**:

| 테스트 유형 | 추천 에이전트 | 비고 |
|-----------|-------------|------|
| TDD (테스트 먼저) | test-engineer | `/tdd` 사용 |
| 단위 테스트 | executor | 간단한 경우 |
| 통합 테스트 | test-engineer | 전문 에이전트 권장 |
| E2E 테스트 | test-engineer | Playwright 등 활용 |
| 커버리지 향상 | test-engineer | 부족한 부분 찾아 추가 |

**실제 사용**:
```bash
# TDD 워크플로우
/oh-my-claudecode:tdd
"Implement user authentication"

# 기존 코드에 테스트 추가
Task(
  subagent_type: "oh-my-claudecode:test-engineer",
  prompt: "Add comprehensive tests for authentication module"
)
```

---

### 7. 문서화

#### 시나리오: "API 문서 작성"

**선택 기준**:

| 문서 유형 | 추천 에이전트 | 모델 |
|----------|-------------|------|
| README | writer | haiku |
| API 문서 | writer | haiku |
| 아키텍처 문서 | architect | opus |
| 마이그레이션 가이드 | writer | haiku |
| 코드 주석 | executor | sonnet |
| 기술 블로그 | writer | haiku |

**실제 사용**:
```typescript
Task(
  subagent_type: "oh-my-claudecode:writer",
  prompt: "Write comprehensive API documentation for user endpoints",
  model: "haiku"
)
```

---

### 8. 성능 최적화

#### 시나리오: "API 응답 속도 개선"

**선택 흐름**:

```
1. 분석
   scientist (sonnet) → 벤치마크 데이터 분석
   debugger (sonnet) → 병목 지점 파악

2. 전략 수립
   architect (opus) → 최적화 전략 리뷰

3. 구현
   executor (sonnet) → 최적화 코드 작성

4. 검증
   scientist (sonnet) → 성능 개선 측정
   verifier (sonnet) → 기능 보존 확인
```

---

### 9. SDK/라이브러리 사용

#### 시나리오: "새로운 라이브러리 도입"

**선택 흐름**:

```
1. 문서 조회 (필수!)
   document-specialist (sonnet)
   → 공식 문서에서 최신 사용법 확인

2. 통합 구현
   executor (sonnet)
   → document-specialist의 정보 기반 구현

3. 테스트
   test-engineer (sonnet)

4. 검증
   verifier (sonnet)
```

**실제 사용**:
```typescript
// 1. 문서 먼저!
Task(
  subagent_type: "oh-my-claudecode:document-specialist",
  prompt: "Look up Prisma ORM latest usage for PostgreSQL"
)

// 2. 구현
Task(
  subagent_type: "oh-my-claudecode:executor",
  prompt: "Integrate Prisma ORM based on documentation"
)
```

---

## 워크플로우별 추천

### Autopilot 모드
**언제**: 완전 자동 실행 원할 때

```bash
/oh-my-claudecode:autopilot
"Build a REST API for task management"
```

**자동 사용 에이전트**:
- explore → analyst → planner → executor → test-engineer → verifier → qa-tester

---

### Ralph 모드
**언제**: 완료까지 자동 실행 + 검증 루프

```bash
/oh-my-claudecode:ralph
"Refactor authentication system"
```

**자동 사용 에이전트**:
- planner → executor (반복) → verifier → architect (검증)

---

### Team 모드
**언제**: 조율된 팀 작업

```bash
/oh-my-claudecode:team
"Implement payment processing"
```

**스테이지별 에이전트**:
- **plan**: explore + planner
- **prd**: analyst + critic
- **exec**: executor + 전문가들
- **verify**: verifier + reviewers
- **fix**: executor/build-fixer/debugger

---

### Ultrawork 모드
**언제**: 최대 병렬 처리

```bash
/oh-my-claudecode:ultrawork
"Add internationalization support"
```

**병렬 실행**:
- 여러 executor 동시 실행
- 독립적 작업들 병렬 처리

---

## 실전 예제

### 예제 1: 새 프로젝트 시작

```bash
# 1. 문서 조회
Task(subagent_type: "oh-my-claudecode:document-specialist",
     prompt: "Look up Next.js 14 App Router best practices")

# 2. 아키텍처 설계
Task(subagent_type: "oh-my-claudecode:architect",
     prompt: "Design architecture for e-commerce platform")

# 3. 계획 수립
/oh-my-claudecode:ralplan
"Plan MVP implementation"

# 4. 실행
/oh-my-claudecode:team
"Implement MVP features"
```

---

### 예제 2: 레거시 코드 개선

```bash
# 1. 탐색
Task(subagent_type: "oh-my-claudecode:explore",
     prompt: "Find all authentication-related code")

# 2. 분석
Task(subagent_type: "oh-my-claudecode:architect",
     prompt: "Analyze current authentication architecture")

# 3. 계획
/oh-my-claudecode:ralplan --deliberate
"Modernize authentication system"

# 4. 실행
/oh-my-claudecode:ralph
"Refactor authentication following the plan"
```

---

### 예제 3: 보안 강화

```bash
# 1. 보안 감사
/oh-my-claudecode:security-review

# 2. 수정
Task(subagent_type: "oh-my-claudecode:executor",
     prompt: "Fix security vulnerabilities identified in review")

# 3. 재검증
Task(subagent_type: "oh-my-claudecode:security-reviewer",
     prompt: "Verify all security issues are resolved")
```

---

## 일반적인 실수

### [금지] 실수 1: 모든 작업에 에이전트 사용
```bash
# 나쁜 예
Task(subagent_type: "oh-my-claudecode:executor",
     prompt: "Read user.ts file")

# 좋은 예
Read(file_path: "src/models/user.ts")
```

---

### [금지] 실수 2: 잘못된 에이전트 선택
```bash
# 나쁜 예 - 탐색에 executor 사용
Task(subagent_type: "oh-my-claudecode:executor",
     prompt: "Find all API routes")

# 좋은 예
Task(subagent_type: "oh-my-claudecode:explore",
     prompt: "Find all API routes")
```

---

### [금지] 실수 3: 문서 조회 생략
```bash
# 나쁜 예 - 직접 구현 시도
Task(subagent_type: "oh-my-claudecode:executor",
     prompt: "Implement Stripe payment integration")

# 좋은 예 - 문서 먼저
Task(subagent_type: "oh-my-claudecode:document-specialist",
     prompt: "Look up Stripe Payment Intents API documentation")
# 그 다음 구현
```

---

### [금지] 실수 4: 검증 생략
```bash
# 나쁜 예 - 구현만 하고 끝
Task(subagent_type: "oh-my-claudecode:executor", ...)

# 좋은 예 - 검증 포함
Task(subagent_type: "oh-my-claudecode:executor", ...)
Task(subagent_type: "oh-my-claudecode:verifier",
     prompt: "Verify feature works correctly")
```

---

### [금지] 실수 5: 잘못된 모델 선택
```bash
# 나쁜 예 - 간단한 작업에 opus
Task(subagent_type: "oh-my-claudecode:explore",
     model: "opus")  # 불필요한 비용

# 좋은 예
Task(subagent_type: "oh-my-claudecode:explore",
     model: "haiku")  # 빠르고 저렴
```

---

## 의사결정 트리

```
작업 시작
│
├─ 무엇을 해야할지 불명확?
│  └─ YES → analyst (opus)
│  └─ NO → 다음
│
├─ 어디서 시작할지 모름?
│  └─ YES → explore (haiku)
│  └─ NO → 다음
│
├─ 계획이 필요한가?
│  └─ YES → planner (opus) 또는 /ralplan
│  └─ NO → 다음
│
├─ 구현 필요?
│  ├─ 간단 → executor (sonnet)
│  ├─ 복잡 → deep-executor (opus)
│  └─ 빌드 실패 → build-fixer (sonnet)
│
├─ 리뷰 필요?
│  ├─ 종합 → code-reviewer (opus)
│  ├─ 보안 → security-reviewer (sonnet)
│  └─ 품질 → quality-reviewer (sonnet)
│
└─ 검증
   └─ verifier (sonnet/opus)
```

---

## 체크리스트

### 에이전트 선택 전
- [ ] 작업 목표가 명확한가?
- [ ] 적절한 에이전트를 선택했는가?
- [ ] 모델 선택이 적절한가?
- [ ] 문서 조회가 필요한가? (SDK/API 사용 시)

### 작업 완료 후
- [ ] 검증 에이전트를 실행했는가?
- [ ] 테스트가 통과하는가?
- [ ] 빌드가 성공하는가?
- [ ] 코드 리뷰를 받았는가?

---

## 참고
- [에이전트 카탈로그](../agent-catalog.md) - 모든 에이전트 상세 정보
- [워크플로우 문서](../workflows/) - 자동화된 워크플로우
- [모델 라우팅](../model-routing.md) - 모델 선택 가이드
