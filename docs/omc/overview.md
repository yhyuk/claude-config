# OMC (oh-my-claudecode) 소개 및 운영 원칙

> oh-my-claudecode는 Claude Code를 위한 지능형 멀티 에이전트 오케스트레이션 레이어입니다.

## 목차
- [OMC란 무엇인가](#omc란-무엇인가)
- [핵심 운영 원칙](#핵심-운영-원칙)
- [OMC의 장점](#omc의-장점)
- [주요 개념](#주요-개념)
- [시작하기](#시작하기)

---

## OMC란 무엇인가

**oh-my-claudecode (OMC)** 는 Claude Code의 멀티 에이전트 오케스트레이션 레이어로, 전문화된 에이전트들을 조율하여 작업을 정확하고 효율적으로 완수합니다.

### 역할
OMC는 다음과 같은 역할을 수행합니다:
- **전문 에이전트 조율**: 각 작업에 가장 적합한 에이전트에게 위임
- **워크플로우 자동화**: 복잡한 작업을 자동으로 단계별로 처리
- **품질 보증**: 검증 에이전트를 통한 완료 확인
- **효율성 극대화**: 병렬 처리 및 최적 경로 선택

### 핵심 가치
- 작업을 **가장 잘하는 에이전트**에게 위임
- 사용자에게 **명확한 진행 상황** 전달
- **증거 기반 검증** - 추측보다 실제 결과 확인
- **최소 비용 경로** 선택 - 품질 유지하며 효율적으로

---

## 핵심 운영 원칙

### 1. 전문화된 위임 (Specialized Delegation)
적절한 전문가에게 작업을 위임합니다.

```
[권장] 올바른 사용:
- 멀티파일 변경 → executor 에이전트
- 코드 리뷰 → code-reviewer 에이전트
- 디버깅 → debugger 에이전트

[금지] 잘못된 사용:
- 간단한 파일 읽기에 에이전트 사용
- 단일 명령어 실행에 에이전트 사용
```

### 2. 증거 기반 작업 (Evidence-Based Work)
가정보다 실제 검증을 우선합니다.

```
[권장] 증거 수집:
1. 변경 사항 확인
2. 테스트 실행
3. 빌드 성공 확인
4. 결과 검증

[금지] 가정:
- "아마 작동할 것이다"
- "테스트가 통과했을 것이다"
```

### 3. 경량 경로 우선 (Lightweight Path First)
품질을 유지하면서 가장 단순한 방법을 선택합니다.

**선택 기준**:
1. **직접 작업** - 단순 작업 (파일 읽기, 단일 명령)
2. **tmux 워커** - 독립적 CLI 작업
3. **에이전트** - 복잡하고 전문적인 작업

### 4. 공식 문서 우선 (Documentation First)
불확실한 SDK/API 사용 시 문서를 먼저 확인합니다.

```
SDK/API 사용 전:
1. document-specialist 에이전트로 공식 문서 조회
2. 최신 사용법 확인
3. 베스트 프랙티스 적용
```

---

## OMC의 장점

### 1. 작업 품질 향상
- **전문 에이전트**: 각 영역의 전문가가 작업 수행
- **자동 검증**: verifier 에이전트가 완료 확인
- **코드 리뷰**: 자동 품질 검사

### 2. 개발 속도 증가
- **병렬 처리**: 여러 에이전트 동시 실행
- **자동화**: 반복 작업 자동 처리
- **빠른 피드백**: 실시간 진행 상황 확인

### 3. 일관성 유지
- **표준화된 패턴**: 검증된 워크플로우 사용
- **자동 컨벤션 적용**: 코드 스타일 자동 준수
- **반복 가능**: 동일한 품질로 작업 재현

### 4. 학습 곡선 감소
- **가이드 제공**: 에이전트가 베스트 프랙티스 제안
- **자동 수정**: 일반적인 실수 자동 감지 및 수정
- **문서화**: 작업 과정 자동 기록

---

## 주요 개념

### 에이전트 (Agents)
특정 작업에 전문화된 독립적인 워커입니다.

**에이전트 유형**:
- **빌드/분석**: explore, analyst, planner, architect, debugger
- **실행**: executor, deep-executor
- **검증**: verifier
- **리뷰**: code-reviewer, security-reviewer, quality-reviewer
- **도메인 전문**: test-engineer, build-fixer, designer, writer

자세한 내용: [에이전트 카탈로그](./agent-catalog.md)

### 워크플로우 (Workflows)
여러 에이전트를 조율하는 자동화된 프로세스입니다.

**주요 워크플로우**:
- **autopilot**: 아이디어부터 작동 코드까지 완전 자동
- **ralph**: 완료까지 자기참조 루프
- **team**: N개의 조율된 에이전트
- **ultrawork**: 최대 병렬 처리

자세한 내용: [워크플로우 문서](./workflows/)

### 모델 라우팅 (Model Routing)
작업의 복잡도에 따라 적절한 AI 모델을 선택합니다.

- **haiku**: 빠른 조회, 간단한 작업
- **sonnet**: 표준 구현 (기본값)
- **opus**: 아키텍처 설계, 심층 분석

자세한 내용: [모델 라우팅 전략](./model-routing.md)

### 상태 관리 (State Management)
작업 진행 상황을 추적하고 관리합니다.

**저장 위치**: `.omc/state/`
- 모드별 상태: `{mode}-state.json`
- 세션별 상태: `sessions/{sessionId}/`

자세한 내용: [상태 관리](./tools/state-management.md)

---

## 시작하기

### 기본 설정

#### 1. OMC 설치 확인
```bash
# OMC가 이미 설치되어 있다면
# CLAUDE.md에 OMC 설정이 포함되어 있어야 합니다
```

#### 2. 첫 번째 명령 실행
```bash
# 계획 수립
/oh-my-claudecode:omc-plan

# 자동 실행
/oh-my-claudecode:autopilot

# 코드 리뷰
/oh-my-claudecode:code-review
```

### 일반적인 사용 패턴

#### 새 기능 개발
```bash
1. /oh-my-claudecode:omc-plan        # 계획 수립
2. /oh-my-claudecode:team            # 팀으로 실행
3. /oh-my-claudecode:code-review     # 리뷰
```

#### 버그 수정
```bash
1. /oh-my-claudecode:analyze         # 분석
2. 직접 수정 또는 /oh-my-claudecode:team
3. 테스트 실행 확인
```

#### 리팩토링
```bash
1. /oh-my-claudecode:ralplan         # 합의 기반 계획
2. /oh-my-claudecode:ralph           # 완료까지 자동 실행
```

### 에이전트 직접 호출
Task 도구로 에이전트를 직접 사용할 수도 있습니다:

```typescript
// 코드 탐색
Task(subagent_type: "oh-my-claudecode:explore",
     prompt: "Find all API endpoints",
     model: "haiku")

// 코드 구현
Task(subagent_type: "oh-my-claudecode:executor",
     prompt: "Implement user authentication",
     model: "sonnet")

// 심층 분석
Task(subagent_type: "oh-my-claudecode:architect",
     prompt: "Review system architecture",
     model: "opus")
```

---

## 위임 규칙

### 에이전트에게 위임해야 하는 경우
- [권장] 멀티파일 변경
- [권장] 리팩토링
- [권장] 디버깅
- [권장] 코드 리뷰
- [권장] 계획 수립
- [권장] 연구/조사
- [권장] 검증
- [권장] 전문 작업 (보안, 성능, 테스트 등)

### 직접 작업해야 하는 경우
- [권장] 단순 작업
- [권장] 작은 명확한 질문
- [권장] 단일 명령 실행
- [권장] 파일 읽기/쓰기 (1-2개)

자세한 내용: [위임 규칙](./delegation-rules.md)

---

## 모범 사례

### 1. 명확한 목표 설정
```
[금지] 나쁜 예: "코드 개선해줘"
[권장] 좋은 예: "UserService의 중복 코드를 제거하고 테스트 커버리지를 80% 이상으로 올려줘"
```

### 2. 적절한 에이전트 선택
```
[금지] 나쁜 예: 모든 작업을 executor로
[권장] 좋은 예:
  - 탐색 → explore
  - 계획 → planner
  - 구현 → executor
  - 검증 → verifier
```

### 3. 검증 필수
```
[권장] 항상 확인:
- 테스트 통과
- 빌드 성공
- 타입 에러 없음
- 기능 작동 확인
```

### 4. 문서화
```
[권장] 변경 사항 기록:
- 커밋 메시지 명확히
- 중요 변경은 문서 업데이트
- CHANGELOG 관리
```

---

## 제한 사항 및 주의사항

### 제한 사항
1. **컨텍스트 크기**: 매우 큰 파일은 나눠서 처리
2. **API 호출 한도**: 병렬 실행 시 주의
3. **복잡도**: 너무 복잡한 작업은 단계별로 분할

### 주의사항
1. **자동 실행 모드**: autopilot/ralph는 자동으로 변경 사항 생성
2. **검증 필수**: 자동 생성 코드는 반드시 검토
3. **비용**: opus 모델은 비용이 높으므로 필요시만 사용

---

## 도움말 및 지원

### 문제 해결
- [트러블슈팅 가이드](../troubleshooting.md)
- [FAQ](../faq.md)

### 추가 문서
- [에이전트 카탈로그](./agent-catalog.md)
- [에이전트 선택 가이드](./agents/selection-guide.md)
- [워크플로우 문서](./workflows/)
- [도구 및 기능](./tools/)

### OMC 명령어
```bash
# 설정
/oh-my-claudecode:omc-setup

# 도움말
/oh-my-claudecode:omc-help

# 진단
/oh-my-claudecode:omc-doctor

# 취소
/oh-my-claudecode:cancel
```

---

## 다음 단계

1. [에이전트 카탈로그](./agent-catalog.md) - 사용 가능한 모든 에이전트 확인
2. [에이전트 선택 가이드](./agents/selection-guide.md) - 상황별 적절한 에이전트 선택법
3. [워크플로우 문서](./workflows/) - autopilot, ralph, team 등 학습
4. [실습 예제](../best-practices.md) - 실제 사용 사례

---

## 참고
- [OMC GitHub](https://github.com/cyanheads/oh-my-claudecode)
- [Claude Code 문서](https://docs.claude.com/claude-code)
