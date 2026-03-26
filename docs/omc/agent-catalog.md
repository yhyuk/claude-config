# 에이전트 카탈로그

> OMC에서 사용 가능한 모든 전문 에이전트의 상세 목록입니다.

## 목차
- [빌드 및 분석 에이전트](#빌드-및-분석-에이전트)
- [실행 에이전트](#실행-에이전트)
- [검증 에이전트](#검증-에이전트)
- [리뷰 에이전트](#리뷰-에이전트)
- [도메인 전문 에이전트](#도메인-전문-에이전트)
- [조율 에이전트](#조율-에이전트)
- [에이전트 사용법](#에이전트-사용법)

---

## 빌드 및 분석 에이전트

### explore (haiku)
**목적**: 코드베이스 탐색 및 검색

**언제 사용**:
- 파일/심볼 찾기
- 코드 패턴 검색
- 프로젝트 구조 파악
- "어디에 X가 정의되어 있나요?" 같은 질문

**특징**:
- 빠른 검색 (haiku 모델)
- 여러 검색 전략 사용
- 파일 매핑 및 패턴 매칭

**예제**:
```typescript
Task(
  subagent_type: "oh-my-claudecode:explore",
  prompt: "Find all API endpoints in the project",
  model: "haiku"
)
```

---

### analyst (opus)
**목적**: 요구사항 분석 및 명확화

**언제 사용**:
- 불명확한 요구사항 정리
- 수용 기준 정의
- 비즈니스 로직 분석
- 프로젝트 계획 수립 전

**특징**:
- 깊이 있는 분석 (opus 모델)
- 질문을 통한 명확화
- 구조화된 요구사항 문서 생성

**예제**:
```typescript
Task(
  subagent_type: "oh-my-claudecode:analyst",
  prompt: "Analyze requirements for user authentication feature",
  model: "opus"
)
```

---

### planner (opus)
**목적**: 작업 계획 및 순서 수립

**언제 사용**:
- 복잡한 기능 구현 전
- 리팩토링 계획
- 마이그레이션 전략
- 단계별 실행 계획 필요 시

**특징**:
- 전략적 계획 수립 (opus 모델)
- 의존성 분석
- 리스크 평가
- 단계별 작업 분해

**예제**:
```typescript
Task(
  subagent_type: "oh-my-claudecode:planner",
  prompt: "Create implementation plan for real-time notification system",
  model: "opus"
)
```

---

### architect (opus)
**목적**: 시스템 설계 및 아키텍처 결정

**언제 사용**:
- 새로운 시스템 설계
- 아키텍처 리뷰
- 기술 스택 결정
- 확장성/보안 설계

**특징**:
- READ-ONLY (코드 변경 안 함)
- 전략적 조언 (opus 모델)
- 인터페이스 경계 설계
- 베스트 프랙티스 제안

**예제**:
```typescript
Task(
  subagent_type: "oh-my-claudecode:architect",
  prompt: "Review microservices architecture for scalability",
  model: "opus"
)
```

---

### debugger (sonnet)
**목적**: 버그 원인 분석 및 수정

**언제 사용**:
- 버그 원인 파악
- 회귀 문제 격리
- 스택 트레이스 분석
- 빌드/컴파일 에러 해결

**특징**:
- 근본 원인 분석 (sonnet 모델)
- 체계적인 디버깅 접근
- 재현 시나리오 생성
- 수정 후 검증

**예제**:
```typescript
Task(
  subagent_type: "oh-my-claudecode:debugger",
  prompt: "Debug null pointer exception in UserService",
  model: "sonnet"
)
```

---

## 실행 에이전트

### executor (sonnet)
**목적**: 코드 구현 및 리팩토링

**언제 사용**:
- 새 기능 구현
- 코드 리팩토링
- 버그 수정 (원인 파악 후)
- 일반적인 코드 변경

**특징**:
- 표준 구현 작업 (sonnet 모델)
- 여러 파일 동시 수정
- 테스트 작성
- 코드 컨벤션 준수

**예제**:
```typescript
Task(
  subagent_type: "oh-my-claudecode:executor",
  prompt: "Implement user profile update API endpoint",
  model: "sonnet"
)
```

---

### deep-executor (opus)
**목적**: 복잡한 자율 실행 작업

**언제 사용**:
- 매우 복잡한 구현
- 여러 시스템 통합
- 자율적 목표 지향 작업
- 고도의 판단이 필요한 경우

**특징**:
- 자율적 실행 (opus 모델)
- 복잡한 의사결정
- 여러 단계의 추론
- 높은 품질 보장

**예제**:
```typescript
Task(
  subagent_type: "oh-my-claudecode:deep-executor",
  prompt: "Implement complete OAuth2 authentication flow with refresh tokens",
  model: "opus"
)
```

---

## 검증 에이전트

### verifier (sonnet/opus)
**목적**: 작업 완료 검증 및 증거 수집

**언제 사용**:
- 구현 완료 후 확인
- 모든 요구사항 충족 확인
- 테스트 통과 검증
- 배포 전 최종 확인

**특징**:
- 증거 기반 검증
- 체크리스트 기반 확인
- 테스트 실행 및 결과 분석
- 완료 보고서 생성

**모델 선택**:
- **haiku**: 간단한 검증 (5개 이하 파일)
- **sonnet**: 표준 검증
- **opus**: 대규모/보안 검증

**예제**:
```typescript
Task(
  subagent_type: "oh-my-claudecode:verifier",
  prompt: "Verify all authentication features are working correctly",
  model: "sonnet"
)
```

---

## 리뷰 에이전트

### code-reviewer (opus)
**목적**: 종합적인 코드 리뷰

**언제 사용**:
- PR/MR 리뷰
- 코드 품질 검사
- API 계약 검토
- 하위 호환성 확인

**특징**:
- 전체적인 코드 리뷰 (opus 모델)
- 로직 결함 감지
- 유지보수성 평가
- 베스트 프랙티스 검증

**예제**:
```bash
/oh-my-claudecode:code-review
```

---

### quality-reviewer (sonnet)
**목적**: 코드 품질 및 성능 리뷰

**언제 사용**:
- 코드 품질 개선
- 성능 최적화
- 안티패턴 감지
- 유지보수성 향상

**특징**:
- 심각도 등급 피드백
- SOLID 원칙 검사
- 성능 이슈 감지
- 리팩토링 제안

**예제**:
```typescript
Task(
  subagent_type: "oh-my-claudecode:quality-reviewer",
  prompt: "Review code quality of payment processing module",
  model: "sonnet"
)
```

---

### security-reviewer (sonnet)
**목적**: 보안 취약점 감지 및 수정

**언제 사용**:
- 보안 감사
- 사용자 입력 처리 후
- 인증/인가 구현 후
- 민감 데이터 처리

**특징**:
- OWASP Top 10 검사
- 시크릿 노출 감지
- 인젝션 취약점 검사
- 보안 베스트 프랙티스

**예제**:
```bash
/oh-my-claudecode:security-review
```

---

## 도메인 전문 에이전트

### test-engineer (sonnet)
**목적**: 테스트 전략 및 구현

**언제 사용**:
- 테스트 전략 수립
- 테스트 커버리지 향상
- Flaky 테스트 수정
- TDD 워크플로우

**특징**:
- 통합/E2E 테스트 전문
- 커버리지 분석
- 테스트 품질 개선
- TDD 가이드

**예제**:
```bash
/oh-my-claudecode:tdd
```

---

### build-fixer (sonnet)
**목적**: 빌드/타입 에러 수정

**언제 사용**:
- 빌드 실패
- TypeScript 타입 에러
- 컴파일 오류
- 도구 체인 문제

**특징**:
- 빌드 에러만 수정
- 최소한의 변경
- 아키텍처 변경 없음
- 빠른 빌드 복구

**예제**:
```bash
/oh-my-claudecode:build-fix
```

---

### designer (sonnet)
**목적**: UI/UX 설계 및 구현

**언제 사용**:
- UI 컴포넌트 설계
- UX 개선
- 반응형 디자인
- 접근성 향상

**특징**:
- 디자인 시스템 준수
- 사용자 경험 최적화
- 시각적 일관성
- 인터랙션 설계

**예제**:
```typescript
Task(
  subagent_type: "oh-my-claudecode:designer",
  prompt: "Design and implement responsive dashboard layout",
  model: "sonnet"
)
```

---

### writer (haiku)
**목적**: 기술 문서 작성

**언제 사용**:
- README 작성
- API 문서화
- 마이그레이션 가이드
- 코드 주석

**특징**:
- 빠른 문서 생성 (haiku 모델)
- 명확하고 간결한 작성
- 사용자 친화적 설명
- 예제 코드 포함

**예제**:
```typescript
Task(
  subagent_type: "oh-my-claudecode:writer",
  prompt: "Write API documentation for user endpoints",
  model: "haiku"
)
```

---

### qa-tester (sonnet)
**목적**: 대화형 CLI 테스팅

**언제 사용**:
- CLI 애플리케이션 테스트
- 서비스 런타임 검증
- tmux 세션 관리
- 대화형 테스트

**특징**:
- tmux 기반 세션 관리
- 실시간 테스트 실행
- 서비스 검증
- 자동화된 QA

**예제**:
```typescript
Task(
  subagent_type: "oh-my-claudecode:qa-tester",
  prompt: "Test CLI application with various user inputs",
  model: "sonnet"
)
```

---

### scientist (sonnet)
**목적**: 데이터 분석 및 연구

**언제 사용**:
- 데이터 분석
- 통계 연구
- 성능 벤치마크
- 실험 및 검증

**특징**:
- Python REPL 활용
- pandas, numpy 지원
- 시각화 (matplotlib)
- 과학적 분석

**예제**:
```typescript
Task(
  subagent_type: "oh-my-claudecode:scientist",
  prompt: "Analyze user behavior patterns from CSV data",
  model: "sonnet"
)
```

---

### document-specialist (sonnet)
**목적**: 외부 문서 조회 및 참조

**언제 사용**:
- 라이브러리 사용법 확인
- 프레임워크 문서 조회
- API 레퍼런스 검색
- 최신 베스트 프랙티스

**특징**:
- 공식 문서 우선
- Context7 MCP 활용
- 최신 정보 제공
- 예제 코드 포함

**예제**:
```typescript
Task(
  subagent_type: "oh-my-claudecode:document-specialist",
  prompt: "Look up Next.js 14 App Router documentation",
  model: "sonnet"
)
```

---

### git-master (sonnet)
**목적**: Git 작업 및 히스토리 관리

**언제 사용**:
- 원자적 커밋 생성
- 리베이스 작업
- 커밋 히스토리 정리
- Git 워크플로우 관리

**특징**:
- 스타일 자동 감지
- 의미 있는 커밋
- 안전한 Git 작업
- 히스토리 관리

**예제**:
```typescript
Task(
  subagent_type: "oh-my-claudecode:git-master",
  prompt: "Create atomic commits for feature implementation",
  model: "sonnet"
)
```

---

### code-simplifier (opus)
**목적**: 코드 단순화 및 리팩토링

**언제 사용**:
- 복잡한 코드 단순화
- 가독성 향상
- 유지보수성 개선
- 일관성 확보

**특징**:
- 기능 보존 (opus 모델)
- 명확성 향상
- 중복 제거
- 최근 변경 코드 우선

**예제**:
```typescript
Task(
  subagent_type: "oh-my-claudecode:code-simplifier",
  prompt: "Simplify complex authentication logic",
  model: "opus"
)
```

---

## 조율 에이전트

### critic (opus)
**목적**: 계획 및 설계 비평

**언제 사용**:
- 계획 검토
- 설계 피드백
- 다각적인 관점 제공
- 리스크 평가

**특징**:
- 비판적 분석 (opus 모델)
- 다양한 관점
- 구조화된 피드백
- 개선 제안

**예제**:
```typescript
Task(
  subagent_type: "oh-my-claudecode:critic",
  prompt: "Review implementation plan for data migration",
  model: "opus"
)
```

---

## 에이전트 사용법

### Task 도구로 직접 호출

```typescript
// 기본 사용법
Task(
  subagent_type: "oh-my-claudecode:executor",
  prompt: "Implement feature X",
  model: "sonnet"  // 선택적
)

// 여러 에이전트 병렬 실행
Task(subagent_type: "oh-my-claudecode:explore", ...)
Task(subagent_type: "oh-my-claudecode:code-reviewer", ...)
```

### Slash 커맨드로 호출

```bash
# 전용 커맨드 (wrapper)
/oh-my-claudecode:code-review
/oh-my-claudecode:security-review
/oh-my-claudecode:build-fix
/oh-my-claudecode:tdd
```

### 워크플로우에서 자동 사용

```bash
# Team 워크플로우
/oh-my-claudecode:team
# → 자동으로 explore, planner, executor, verifier 조율

# Autopilot
/oh-my-claudecode:autopilot
# → 전체 파이프라인 자동 실행
```

---

## 모델 선택 가이드

### haiku (빠름, 저렴)
- explore
- writer
- 간단한 verifier

### sonnet (균형, 기본값)
- executor
- debugger
- quality-reviewer
- security-reviewer
- test-engineer
- build-fixer
- 대부분의 작업

### opus (강력, 고비용)
- analyst
- planner
- architect
- deep-executor
- code-reviewer
- critic
- code-simplifier

---

## 언어별 전문 에이전트

### Python
- **python-reviewer**: PEP 8, Pythonic 관용구, 타입 힌트

### Rust
- **rust-reviewer**: 소유권, 라이프타임, 에러 처리
- **rust-build-resolver**: Cargo 빌드 에러 수정

### C++
- **cpp-reviewer**: 메모리 안전성, 현대 C++ 관용구
- **cpp-build-resolver**: CMake, 링커 에러 수정

### Java/Spring
- **java-reviewer**: 레이어 아키텍처, JPA 패턴
- **java-build-resolver**: Maven/Gradle 빌드 수정

### Go
- **go-reviewer**: 관용적 Go, 동시성 패턴
- **go-build-resolver**: Go 빌드 수정

### Kotlin
- **kotlin-reviewer**: 관용적 Kotlin, 코루틴, Compose
- **kotlin-build-resolver**: Gradle 빌드 수정

---

## 에이전트 선택 플로우차트

```
작업 유형?
│
├─ 탐색/조사 → explore (haiku)
├─ 계획 필요 → planner (opus)
├─ 설계/아키텍처 → architect (opus)
├─ 구현
│  ├─ 단순 → executor (sonnet)
│  └─ 복잡 → deep-executor (opus)
├─ 디버깅 → debugger (sonnet)
├─ 빌드 실패 → build-fixer (sonnet)
├─ 리뷰
│  ├─ 종합 → code-reviewer (opus)
│  ├─ 보안 → security-reviewer (sonnet)
│  └─ 품질 → quality-reviewer (sonnet)
├─ 테스트 → test-engineer (sonnet)
├─ 검증 → verifier (sonnet/opus)
├─ 문서화 → writer (haiku)
└─ 데이터 분석 → scientist (sonnet)
```

---

## 참고
- [에이전트 선택 가이드](./agents/selection-guide.md) - 상황별 상세 가이드
- [모델 라우팅](./model-routing.md) - 모델 선택 전략
- [워크플로우](./workflows/) - 에이전트 조율 방법
