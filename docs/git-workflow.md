# Git 워크플로우

> 프로젝트의 Git 브랜치 전략 및 협업 워크플로우 가이드입니다.

## 목차
- [브랜치 전략](#브랜치-전략)
- [브랜치 네이밍 규칙](#브랜치-네이밍-규칙)
- [작업 흐름](#작업-흐름)
- [커밋 규칙](#커밋-규칙)
- [코드 리뷰](#코드-리뷰)
- [병합 전략](#병합-전략)
- [OMC Git 도구](#omc-git-도구)

---

## 브랜치 전략

### Git Flow (권장)

프로젝트 규모가 크고 릴리스 주기가 명확한 경우 사용합니다.

```
main (production)
  ├── develop (개발 통합)
  │   ├── feature/user-auth (기능 개발)
  │   ├── feature/payment (기능 개발)
  │   └── bugfix/login-error (버그 수정)
  ├── release/v1.0.0 (릴리스 준비)
  └── hotfix/critical-bug (긴급 수정)
```

#### 주요 브랜치

**main (또는 master)**
- 프로덕션 배포 브랜치
- 항상 배포 가능한 상태 유지
- 직접 커밋 금지
- 태그로 버전 관리

**develop**
- 다음 릴리스 개발 통합 브랜치
- feature 브랜치들이 merge되는 곳
- 안정적인 상태 유지

#### 보조 브랜치

**feature/**
- 새로운 기능 개발
- develop에서 분기
- develop으로 merge

**release/**
- 릴리스 준비 (버그 수정, 문서화)
- develop에서 분기
- main과 develop에 모두 merge

**hotfix/**
- 프로덕션 긴급 버그 수정
- main에서 분기
- main과 develop에 모두 merge

---

### GitHub Flow (간소화)

소규모 팀이나 지속적 배포 환경에 적합합니다.

```
main (production)
  ├── feature/user-profile
  ├── fix/login-redirect
  └── docs/api-documentation
```

#### 특징
- main 브랜치만 영구 유지
- 모든 작업은 feature 브랜치에서
- PR(Pull Request)을 통한 merge
- main에 merge = 즉시 배포

---

### Trunk-Based Development

매우 빠른 배포 주기와 작은 변경을 선호하는 경우 사용합니다.

```
main (trunk)
  ├── short-lived feature branches (1-2일)
```

#### 특징
- main 브랜치에 자주 통합 (최소 하루 1회)
- 짧은 생명주기의 feature 브랜치
- Feature Flag로 미완성 기능 숨김
- CI/CD 필수

---

## 브랜치 네이밍 규칙

### 형식
```
<type>/<description>
```

### Type 분류

| Type | 설명 | 예시 |
|------|------|------|
| `feature/` | 새로운 기능 | `feature/user-authentication` |
| `bugfix/` | 버그 수정 | `bugfix/login-redirect` |
| `hotfix/` | 긴급 버그 수정 | `hotfix/security-patch` |
| `release/` | 릴리스 준비 | `release/v1.2.0` |
| `refactor/` | 리팩토링 | `refactor/user-service` |
| `docs/` | 문서 작업 | `docs/api-guide` |
| `test/` | 테스트 추가/수정 | `test/user-service` |
| `chore/` | 빌드, 설정 등 | `chore/update-dependencies` |

### Description 규칙
- 소문자, 하이픈(-) 사용
- 간결하고 설명적
- 이슈 번호 포함 가능

```bash
# ✅ 좋은 예
feature/user-profile-update
bugfix/null-pointer-in-auth
hotfix/payment-gateway-timeout
release/v2.1.0

# ❌ 나쁜 예
feature/User_Profile  # 대문자, 언더스코어
mywork  # 의미 불명확
feature/fix  # type과 description 불일치
```

---

## 작업 흐름

### 1. 새로운 작업 시작

#### Git Flow 사용 시
```bash
# 1. develop 브랜치로 이동
git checkout develop

# 2. 최신 상태로 업데이트
git pull origin develop

# 3. 새 feature 브랜치 생성
git checkout -b feature/user-authentication

# 4. 작업 시작
# ... 코딩 ...
```

#### GitHub Flow 사용 시
```bash
# 1. main 브랜치로 이동
git checkout main

# 2. 최신 상태로 업데이트
git pull origin main

# 3. 새 브랜치 생성
git checkout -b feature/user-authentication

# 4. 작업 시작
```

---

### 2. 작업 중

```bash
# 변경사항 확인
git status
git diff

# 스테이징
git add <files>
# 또는 모든 변경사항
git add .

# 커밋 (아래 커밋 규칙 참조)
git commit -m "feat: add user authentication"

# 원격에 푸시
git push origin feature/user-authentication

# 첫 푸시 시
git push -u origin feature/user-authentication
```

---

### 3. PR(Pull Request) 생성

```bash
# GitHub CLI 사용 (권장)
gh pr create --title "feat: User authentication" \
  --body "Implements user login and registration"

# 또는 OMC git-master 사용
Task(
  subagent_type: "oh-my-claudecode:git-master",
  prompt: "Create PR for user authentication feature"
)
```

#### PR 템플릿
```markdown
## Summary
간단한 변경 내용 요약

## Changes
- Added user login endpoint
- Implemented JWT token generation
- Added unit tests

## Test Plan
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Manual testing completed

## Screenshots (if applicable)
[스크린샷 첨부]

## Related Issues
Closes #123
```

---

### 4. 코드 리뷰 및 수정

```bash
# 리뷰 피드백 반영
# ... 코드 수정 ...

# 추가 커밋
git add .
git commit -m "fix: address review comments"
git push origin feature/user-authentication
```

---

### 5. Merge

#### Squash and Merge (권장)
- 여러 커밋을 하나로 합침
- 깔끔한 히스토리 유지

```bash
# GitHub에서 "Squash and merge" 버튼 클릭
# 또는 로컬에서
git checkout develop
git merge --squash feature/user-authentication
git commit -m "feat: add user authentication"
```

#### Merge Commit
- 모든 커밋 보존
- 브랜치 히스토리 유지

```bash
git checkout develop
git merge --no-ff feature/user-authentication
```

#### Rebase and Merge
- 선형 히스토리
- 깔끔한 로그

```bash
git checkout feature/user-authentication
git rebase develop
git checkout develop
git merge feature/user-authentication
```

---

### 6. 브랜치 정리

```bash
# 로컬 브랜치 삭제
git branch -d feature/user-authentication

# 원격 브랜치 삭제
git push origin --delete feature/user-authentication

# 또는 GitHub에서 "Delete branch" 버튼
```

---

## 커밋 규칙

### Conventional Commits

형식: `<type>(<scope>): <subject>`

```bash
feat(auth): add user login endpoint
fix(payment): resolve null pointer in checkout
docs(readme): update installation guide
refactor(user): simplify validation logic
test(auth): add integration tests
chore(deps): update dependencies
```

### Type 분류

| Type | 설명 | 예시 |
|------|------|------|
| `feat` | 새로운 기능 | `feat: add user registration` |
| `fix` | 버그 수정 | `fix: resolve login redirect issue` |
| `docs` | 문서 변경 | `docs: update API documentation` |
| `style` | 코드 포맷팅 (기능 변경 없음) | `style: format code with prettier` |
| `refactor` | 리팩토링 | `refactor: simplify auth logic` |
| `test` | 테스트 추가/수정 | `test: add unit tests for UserService` |
| `chore` | 빌드, 설정 등 | `chore: update webpack config` |
| `perf` | 성능 개선 | `perf: optimize database queries` |

### Subject 작성 규칙

```bash
# ✅ 좋은 예
feat: add user authentication
fix: resolve payment processing error
docs: update installation guide

# ❌ 나쁜 예
feat: Added user authentication  # 과거형
fix: fixed bug  # 불명확
update code  # type 없음
```

### Scope (선택)
```bash
feat(auth): add JWT token validation
fix(payment): resolve Stripe integration bug
docs(api): add endpoint documentation
```

### Body (선택 - 상세 설명)
```bash
git commit -m "feat: add user authentication" -m "
- Implement login endpoint
- Add JWT token generation
- Include password hashing with bcrypt
"
```

### Footer (선택 - 이슈 참조)
```bash
git commit -m "fix: resolve login redirect" -m "
Fixes #123
Closes #124
"
```

---

## OMC를 통한 커밋

### git-master 에이전트 사용

```typescript
// 자동으로 의미있는 커밋 생성
Task(
  subagent_type: "oh-my-claudecode:git-master",
  prompt: "Create atomic commits for the authentication feature"
)
```

**특징**:
- 스타일 자동 감지
- 의미있는 커밋 메시지
- 원자적 커밋 생성
- 커밋 히스토리 관리

### 일반 커밋 가이드라인 (Claude Code 기본)

커밋 요청 시 Claude Code는 다음 단계를 수행합니다:

1. **git status** - 변경사항 확인
2. **git diff** - 변경 내용 분석
3. **git log** - 커밋 스타일 파악
4. **커밋 메시지 작성** - 프로젝트 스타일 준수
5. **git add** - 관련 파일 스테이징
6. **git commit** - 의미있는 메시지로 커밋

---

## 코드 리뷰

### 리뷰 체크리스트

#### 기능
- [ ] 요구사항 충족
- [ ] 엣지 케이스 처리
- [ ] 에러 처리

#### 코드 품질
- [ ] 코드 스타일 준수
- [ ] 네이밍 명확
- [ ] 중복 코드 없음
- [ ] 적절한 추상화

#### 테스트
- [ ] 테스트 코드 존재
- [ ] 테스트 통과
- [ ] 커버리지 충분

#### 보안
- [ ] 입력 검증
- [ ] 인증/인가 확인
- [ ] 민감 정보 노출 없음

### OMC 자동 리뷰

```bash
# 종합 코드 리뷰
/oh-my-claudecode:code-review

# 보안 리뷰
/oh-my-claudecode:security-review

# 병렬 실행
Task(subagent_type: "oh-my-claudecode:code-reviewer", ...)
Task(subagent_type: "oh-my-claudecode:security-reviewer", ...)
```

---

## 병합 전략

### Squash and Merge (권장 - 대부분의 경우)

**장점**:
- 깔끔한 히스토리
- 하나의 의미있는 커밋
- 실험적 커밋 숨김

**단점**:
- 상세 작업 과정 손실

**사용 시기**:
- Feature 브랜치 → develop
- 여러 실험적 커밋이 있는 경우

```bash
git checkout develop
git merge --squash feature/user-auth
git commit -m "feat: add user authentication"
```

---

### Merge Commit (Feature Flag 사용 시)

**장점**:
- 모든 커밋 보존
- 브랜치 히스토리 명확

**단점**:
- 복잡한 히스토리

**사용 시기**:
- 장기 feature 브랜치
- 여러 개발자 협업

```bash
git checkout develop
git merge --no-ff feature/user-auth
```

---

### Rebase and Merge (선형 히스토리 선호 시)

**장점**:
- 선형 히스토리
- 각 커밋 보존

**단점**:
- 충돌 해결 복잡

**사용 시기**:
- 깨끗한 커밋 히스토리가 있는 경우
- 선형 히스토리 선호

```bash
git checkout feature/user-auth
git rebase develop
# 충돌 해결
git checkout develop
git merge feature/user-auth
```

---

## 충돌 해결

### 1. 충돌 발생 시

```bash
# merge 또는 rebase 시 충돌 발생
git status  # 충돌 파일 확인
```

### 2. 충돌 해결

```typescript
// 충돌 파일 예시
<<<<<<< HEAD
const apiUrl = 'https://api.example.com';
=======
const apiUrl = 'https://api-v2.example.com';
>>>>>>> feature/new-api

// 수동으로 해결
const apiUrl = 'https://api-v2.example.com';
```

### 3. OMC 활용

```typescript
// debugger 에이전트로 충돌 분석
Task(
  subagent_type: "oh-my-claudecode:debugger",
  prompt: "Analyze and resolve merge conflicts"
)
```

### 4. 완료

```bash
# 해결된 파일 스테이징
git add <resolved-files>

# merge 계속
git merge --continue

# 또는 rebase 계속
git rebase --continue
```

---

## 릴리스 워크플로우

### 1. Release 브랜치 생성

```bash
# develop에서 분기
git checkout develop
git pull origin develop
git checkout -b release/v1.2.0
```

### 2. 버전 업데이트

```bash
# package.json, build.gradle 등 버전 업데이트
git add .
git commit -m "chore: bump version to 1.2.0"
```

### 3. 버그 수정 (필요 시)

```bash
# 릴리스 브랜치에서 버그 수정
git commit -m "fix: resolve issue before release"
```

### 4. Merge to main

```bash
git checkout main
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin main --tags
```

### 5. Merge back to develop

```bash
git checkout develop
git merge --no-ff release/v1.2.0
git push origin develop
```

### 6. 브랜치 삭제

```bash
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0
```

---

## Hotfix 워크플로우

### 긴급 버그 수정

```bash
# 1. main에서 hotfix 브랜치 생성
git checkout main
git checkout -b hotfix/critical-security-issue

# 2. 버그 수정
git commit -m "fix: resolve critical security vulnerability"

# 3. main에 merge
git checkout main
git merge --no-ff hotfix/critical-security-issue
git tag -a v1.2.1 -m "Hotfix: security patch"
git push origin main --tags

# 4. develop에도 merge
git checkout develop
git merge --no-ff hotfix/critical-security-issue
git push origin develop

# 5. 브랜치 삭제
git branch -d hotfix/critical-security-issue
```

---

## OMC Git 도구

### git-master 에이전트

```bash
# 원자적 커밋 생성
Task(
  subagent_type: "oh-my-claudecode:git-master",
  prompt: "Create atomic commits for feature implementation"
)

# 리베이스 작업
Task(
  subagent_type: "oh-my-claudecode:git-master",
  prompt: "Rebase feature branch on develop"
)

# 커밋 히스토리 정리
Task(
  subagent_type: "oh-my-claudecode:git-master",
  prompt: "Clean up commit history before merge"
)
```

**특징**:
- 스타일 자동 감지
- 안전한 Git 작업
- 의미있는 커밋 메시지
- 히스토리 관리

---

## 모범 사례

### 1. 자주 커밋, 자주 푸시
```bash
# 작은 단위로 자주 커밋
# 하루에 여러 번 푸시
```

### 2. main/develop 직접 커밋 금지
```bash
# 항상 브랜치에서 작업
# PR을 통해서만 merge
```

### 3. 커밋 전 테스트
```bash
# 테스트 실행
npm test

# 빌드 확인
npm run build

# 그 후 커밋
git commit
```

### 4. 의미있는 커밋 메시지
```bash
# ✅ 좋은 예
git commit -m "feat: add user authentication with JWT"

# ❌ 나쁜 예
git commit -m "update"
git commit -m "fix bug"
```

### 5. 브랜치는 짧게 유지
```bash
# Feature 브랜치: 1-3일
# 너무 길면 분할 고려
```

---

## 체크리스트

### 브랜치 생성 전
- [ ] 최신 코드로 업데이트 (`git pull`)
- [ ] 올바른 베이스 브랜치에서 분기
- [ ] 브랜치 네이밍 규칙 준수

### 커밋 전
- [ ] 테스트 통과
- [ ] 코드 스타일 검사
- [ ] 불필요한 파일 제외 (.gitignore)
- [ ] 의미있는 커밋 메시지

### PR 생성 전
- [ ] 모든 변경사항 커밋
- [ ] 원격 브랜치에 푸시
- [ ] 충돌 해결
- [ ] PR 템플릿 작성

### Merge 전
- [ ] 코드 리뷰 승인
- [ ] CI/CD 통과
- [ ] 충돌 없음
- [ ] 테스트 모두 통과

---

## 참고
- [커밋 메시지 규칙](./commit-conventions.md)
- [PR/MR 가이드](./pr-guidelines.md)
- [코드 리뷰 체크리스트](./code-review.md)
- [OMC git-master 에이전트](./omc/agents/domain-specialists.md)
