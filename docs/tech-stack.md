# 기술 스택

> 프로젝트에서 사용하는 기술 스택과 각 기술의 역할 및 선택 이유를 설명합니다.

## 개요

이 문서는 프로젝트의 기술 선택 기준과 각 기술의 용도를 설명합니다.
새로운 기술 도입 시 이 문서를 업데이트하세요.

## 핵심 기술 스택

### 언어
- **TypeScript** (v5.x)
  - 정적 타입 검사로 런타임 오류 방지
  - 코드 자동완성 및 리팩토링 지원
  - JavaScript와의 호환성

### 프레임워크
- **[프레임워크 이름]** (버전)
  - 선택 이유: [성능, 생태계, 팀 경험 등]
  - 주요 사용 패턴: [컴포넌트 기반, 함수형 등]

### 빌드 도구
- **[빌드 도구]** (버전)
  - 번들링 및 최적화
  - 개발 서버 제공
  - Hot Module Replacement (HMR)

## 프론트엔드 (해당 시)

### UI 프레임워크
- **React** / **Vue** / **Next.js** 등
  - 버전:
  - 선택 이유:

### 상태 관리
- **[상태 관리 라이브러리]**
  - 전역 상태 관리
  - 서버 상태 캐싱

### 스타일링
- **[CSS 프레임워크/라이브러리]**
  - Tailwind CSS / CSS Modules / Styled Components 등
  - 선택 이유:

### UI 컴포넌트
- **[컴포넌트 라이브러리]**
  - Material UI / Ant Design / shadcn/ui 등

## 백엔드 (해당 시)

### 런타임/프레임워크
- **Node.js** / **Bun** / **Deno**
  - 버전:
  - 프레임워크: Express / Fastify / Nest.js 등

### 데이터베이스
- **[데이터베이스]**
  - PostgreSQL / MySQL / MongoDB 등
  - ORM/ODM: Prisma / TypeORM / Mongoose 등
  - 선택 이유:

### API
- **REST** / **GraphQL** / **tRPC**
  - API 스타일 선택 이유:
  - 문서화 도구: Swagger / GraphiQL 등

### 인증/인가
- **[인증 솔루션]**
  - JWT / Session / OAuth2.0
  - 라이브러리: Passport / NextAuth 등

## 테스팅

### 단위 테스트
- **[테스트 프레임워크]**
  - Jest / Vitest / Mocha 등
  - 커버리지 도구:

### E2E 테스트
- **[E2E 프레임워크]**
  - Playwright / Cypress / Puppeteer
  - 선택 이유:

### 테스트 유틸리티
- **Testing Library** / **Enzyme**
  - 컴포넌트 테스팅

## 개발 도구

### 코드 품질
- **ESLint** - 코드 린팅
- **Prettier** - 코드 포맷팅
- **TypeScript** - 타입 검사
- **Husky** - Git hooks 관리

### 버전 관리
- **Git**
- **GitHub** / **GitLab** / **Bitbucket**

### CI/CD
- **[CI/CD 플랫폼]**
  - GitHub Actions / GitLab CI / Jenkins
  - 배포 자동화

## 인프라 및 배포

### 호스팅
- **[호스팅 플랫폼]**
  - Vercel / Netlify / AWS / GCP / Azure
  - 선택 이유:

### 컨테이너화
- **Docker** (해당 시)
  - 환경 일관성
  - 배포 단순화

### 모니터링
- **[모니터링 도구]**
  - Sentry / DataDog / New Relic
  - 로깅: Winston / Pino

## 라이브러리 및 유틸리티

### 날짜/시간
- **date-fns** / **dayjs** / **Luxon**

### HTTP 클라이언트
- **axios** / **fetch API** / **ky**

### 폼 관리
- **React Hook Form** / **Formik** / **Zod**

### 유효성 검증
- **Zod** / **Yup** / **Joi**

## 기술 선택 기준

새로운 기술 도입 시 다음을 고려합니다:

1. **필요성**
   - 기존 기술로 해결 불가능한가?
   - 명확한 문제를 해결하는가?

2. **성숙도**
   - 프로덕션 사용 사례가 충분한가?
   - 활발한 유지보수가 이루어지는가?
   - 커뮤니티가 활성화되어 있는가?

3. **팀 역량**
   - 팀이 학습 가능한 난이도인가?
   - 러닝 커브가 적절한가?

4. **생태계**
   - 기존 스택과 잘 통합되는가?
   - 필요한 플러그인/확장이 있는가?

5. **성능**
   - 프로젝트 규모에 적합한가?
   - 벤치마크 결과가 만족스러운가?

6. **라이선스**
   - 상용 사용이 가능한가?
   - 라이선스 충돌이 없는가?

## 버전 관리 정책

### 메이저 버전 업데이트
- 최소 3개월 검토 기간
- 마이그레이션 가이드 작성 필수
- 충분한 테스트 후 적용

### 마이너/패치 업데이트
- 보안 패치는 즉시 적용
- 기능 추가는 검토 후 적용
- Breaking changes 없음 확인

## 의존성 관리

### 패키지 매니저
- **npm** / **yarn** / **pnpm** / **bun**
  - 선택한 매니저:
  - Lock 파일 반드시 커밋

### 의존성 분류
- **dependencies**: 프로덕션 필수 패키지
- **devDependencies**: 개발 도구
- **peerDependencies**: 호환성 정의

### 보안
- 정기적인 `npm audit` / `yarn audit` 실행
- Dependabot / Renovate로 자동 업데이트

## 레거시 및 제거 예정

### 제거 예정 기술
| 기술 | 제거 이유 | 대체 기술 | 예정일 |
|-----|----------|----------|--------|
| - | - | - | - |

## 참고 문서
- [아키텍처 개요](./architecture.md)
- [개발 환경 설정](./dev-setup.md)
- [의존성 관리](./dependency-management.md)

## 업데이트 이력

이 섹션에 기술 스택 변경 이력을 기록합니다.

| 날짜 | 변경 내용 | 담당자 |
|-----|----------|--------|
| YYYY-MM-DD | 프로젝트 초기 설정 | - |
