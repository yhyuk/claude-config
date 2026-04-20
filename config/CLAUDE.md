# CLAUDE.md - 글로벌 가이드

## 기본 규칙
- 이모지 사용 지양
- 다양한 플러그인을 사용하더라도 무조건 한국어로 응답할 것

## 플러그인 역할 분담

### OMC (oh-my-claudecode) — 주 워크플로우 엔진
- 계획: `/oh-my-claudecode:ralplan` (합의 기반), `ralplan --deliberate` (고위험)
- 실행: `/oh-my-claudecode:autopilot`, `ralph`, `team`, `ultrawork`
- 디버깅: `/oh-my-claudecode:analyze`
- 리뷰: OMC code-reviewer, security-reviewer
- 취소: `/oh-my-claudecode:cancel`

### ECC (everything-claude-code) — Spring Boot 전문 도구 (자동 동작)
- 빌드 에러 시: java-build-resolver, springboot-patterns 에이전트가 자동 개입
- 문서 조회: docs-lookup 에이전트 (context7 기반 라이브러리 문서 조회)
- 학습: `/everything-claude-code:learn-eval`, `/instinct-status`

## 상황별 에이전트

| 상황 | 에이전트 |
|------|---------|
| 탐색/조사 | `oh-my-claudecode:explore` (haiku) |
| 외부 문서 조회 | `oh-my-claudecode:document-specialist` |
| 아키텍처 설계 | `oh-my-claudecode:architect` (opus) |
| 일반 구현 | `oh-my-claudecode:executor` (sonnet) |
| 복잡한 구현 | `oh-my-claudecode:deep-executor` (opus) |

## 보안
- 절대 커밋 금지: `.env`, `credentials.json`, API keys
- 환경 변수 사용, Secrets Manager 활용

## Git 커밋 규칙 (Conventional Commits)
```
feat: 새로운 기능
fix: 버그 수정
docs: 문서 변경
refactor: 리팩토링
test: 테스트 추가/수정
chore: 빌드, 설정 등
```
