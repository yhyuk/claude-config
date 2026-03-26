# 프로젝트 구조

> 프로젝트의 디렉토리 구조와 각 폴더의 역할을 설명합니다.

## 목차
- [프론트엔드 프로젝트 구조](#프론트엔드-프로젝트-구조)
- [백엔드 (Spring Boot) 프로젝트 구조](#백엔드-spring-boot-프로젝트-구조)
- [모노레포 구조](#모노레포-구조)

---

## 프론트엔드 프로젝트 구조

### 기본 디렉토리 구조

```
frontend-project/
├── .claude/              # Claude Code 설정 및 문서
│   ├── CLAUDE.md        # 프로젝트 가이드 인덱스
│   ├── docs/            # 상세 문서들
│   └── commands/        # 커스텀 slash 커맨드
├── src/                 # 소스 코드
├── tests/               # 테스트 파일
├── public/              # 정적 파일
├── docs/                # 사용자 대상 문서
├── scripts/             # 빌드/배포 스크립트
└── config/              # 설정 파일
```

### 주요 디렉토리 상세

#### `.claude/`
Claude Code 관련 설정과 프로젝트 가이드라인을 관리합니다.

- **CLAUDE.md**: 프로젝트 전체 가이드의 목차 (이 문서의 인덱스)
- **docs/**: 각 주제별 상세 가이드 문서
- **commands/**: 프로젝트별 커스텀 slash 커맨드

#### `src/` (Frontend)
프론트엔드 애플리케이션의 소스 코드를 포함합니다.

```
src/
├── components/          # 재사용 가능한 컴포넌트
├── pages/              # 페이지/라우트
├── utils/              # 유틸리티 함수
├── hooks/              # 커스텀 훅 (React)
├── services/           # API 서비스
├── stores/             # 상태 관리 (Zustand, Redux 등)
├── types/              # 타입 정의
├── constants/          # 상수 정의
├── styles/             # 전역 스타일
└── assets/             # 이미지, 폰트 등
```

### `tests/`
테스트 코드를 관리합니다.

```
tests/
├── unit/               # 단위 테스트
├── integration/        # 통합 테스트
├── e2e/                # E2E 테스트
└── fixtures/           # 테스트 데이터
```

### `docs/`
사용자 및 개발자를 위한 문서를 관리합니다.

- API 문서
- 사용자 가이드
- 아키텍처 다이어그램

### `scripts/`
빌드, 배포, 데이터 마이그레이션 등의 스크립트를 관리합니다.

### `config/`
환경별 설정 파일을 관리합니다.

```
config/
├── development.json
├── staging.json
└── production.json
```

## 파일 네이밍 규칙

### 일반 규칙
- 소문자와 하이픈 사용: `user-profile.ts`
- 명확하고 설명적인 이름 사용
- 확장자는 파일 종류를 명확히 나타냄

### 컴포넌트
- PascalCase 사용: `UserProfile.tsx`
- 인덱스 파일: `index.ts` (re-export용)

### 테스트 파일
- 원본 파일명 + `.test` 또는 `.spec`:
  - `user-profile.test.ts`
  - `UserProfile.spec.tsx`

### 타입 정의
- `.types.ts` 접미사: `user.types.ts`
- 또는 `types/` 디렉토리에 집중 관리

## 모듈 구조 원칙

### 1. 기능별 그룹핑
연관된 파일들은 같은 디렉토리에 배치합니다.

```
src/features/user/
├── UserProfile.tsx
├── UserSettings.tsx
├── user.service.ts
├── user.types.ts
└── index.ts
```

### 2. 레이어 분리
UI, 비즈니스 로직, 데이터 레이어를 분리합니다.

```
src/
├── components/         # UI 레이어
├── services/          # 비즈니스 로직
└── repositories/      # 데이터 레이어
```

### 3. 공통 모듈
여러 곳에서 사용되는 코드는 `common/` 또는 `shared/`에 배치합니다.

```
src/common/
├── utils/
├── hooks/
├── components/
└── types/
```

## 임포트 경로 규칙

### 절대 경로 사용 (권장)
```typescript
import { UserProfile } from '@/components/UserProfile';
import { formatDate } from '@/utils/date';
```

### 상대 경로
같은 디렉토리 또는 가까운 파일만 상대 경로 사용:
```typescript
import { UserService } from './user.service';
import { UserType } from './user.types';
```

## 특수 파일

### 설정 파일
프로젝트 루트에 위치:
- `package.json` - 의존성 관리
- `tsconfig.json` - TypeScript 설정
- `.gitignore` - Git 무시 파일
- `.env` - 환경 변수 (절대 커밋 금지)
- `.env.example` - 환경 변수 템플릿

### README
각 주요 디렉토리에 `README.md` 배치하여 해당 모듈 설명

---

## 백엔드 (Spring Boot) 프로젝트 구조

### 기본 디렉토리 구조

```
backend-spring-project/
├── .claude/                      # Claude Code 설정 및 문서
│   ├── CLAUDE.md
│   ├── docs/
│   └── commands/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/project/
│   │   │       ├── ProjectApplication.java    # 메인 애플리케이션
│   │   │       ├── config/                     # 설정 클래스
│   │   │       ├── controller/                 # REST 컨트롤러
│   │   │       ├── service/                    # 비즈니스 로직
│   │   │       ├── repository/                 # 데이터 접근 계층
│   │   │       ├── domain/                     # 엔티티 (또는 entity/)
│   │   │       ├── dto/                        # DTO (Data Transfer Object)
│   │   │       ├── exception/                  # 커스텀 예외
│   │   │       ├── util/                       # 유틸리티 클래스
│   │   │       └── security/                   # 보안 관련
│   │   └── resources/
│   │       ├── application.yml                 # 설정 파일
│   │       ├── application-dev.yml             # 개발 환경
│   │       ├── application-prod.yml            # 프로덕션 환경
│   │       ├── static/                         # 정적 리소스
│   │       ├── templates/                      # 템플릿 (Thymeleaf 등)
│   │       └── db/migration/                   # DB 마이그레이션 (Flyway/Liquibase)
│   └── test/
│       ├── java/
│       │   └── com/example/project/
│       │       ├── controller/                 # 컨트롤러 테스트
│       │       ├── service/                    # 서비스 테스트
│       │       ├── repository/                 # 레포지토리 테스트
│       │       └── integration/                # 통합 테스트
│       └── resources/
│           └── application-test.yml            # 테스트 설정
├── docs/                                       # API 문서, ERD 등
├── scripts/                                    # 배포/빌드 스크립트
├── build.gradle (또는 pom.xml)                 # 빌드 설정
├── .gitignore
└── README.md
```

### Spring Boot 레이어 아키텍처

#### 1. Controller Layer
- HTTP 요청/응답 처리
- 요청 유효성 검증
- DTO 변환

```java
// UserController.java
@RestController
@RequestMapping("/api/users")
public class UserController {
    // GET, POST, PUT, DELETE 엔드포인트
}
```

#### 2. Service Layer
- 비즈니스 로직 구현
- 트랜잭션 관리
- 여러 Repository 조합

```java
// UserService.java
@Service
@Transactional
public class UserService {
    // 비즈니스 로직
}
```

#### 3. Repository Layer
- 데이터 접근 로직
- JPA, MyBatis 등 사용
- 엔티티와 직접 상호작용

```java
// UserRepository.java
public interface UserRepository extends JpaRepository<User, Long> {
    // 쿼리 메서드
}
```

#### 4. Domain/Entity Layer
- 데이터베이스 테이블과 매핑
- 비즈니스 규칙 포함 가능

```java
// User.java
@Entity
@Table(name = "users")
public class User {
    // 필드, getter/setter, 비즈니스 메서드
}
```

### 패키지 구조 전략

#### 기능 기반 패키징 (Feature-based) - 권장
```
com.example.project/
├── user/
│   ├── UserController.java
│   ├── UserService.java
│   ├── UserRepository.java
│   ├── User.java (엔티티)
│   └── dto/
│       ├── UserCreateDto.java
│       └── UserResponseDto.java
├── order/
│   ├── OrderController.java
│   ├── OrderService.java
│   ├── OrderRepository.java
│   └── Order.java
└── common/
    ├── config/
    ├── exception/
    └── util/
```

**장점**: 기능별로 응집도 높음, 모듈화 용이

#### 레이어 기반 패키징 (Layer-based) - 전통적
```
com.example.project/
├── controller/
│   ├── UserController.java
│   └── OrderController.java
├── service/
│   ├── UserService.java
│   └── OrderService.java
├── repository/
│   ├── UserRepository.java
│   └── OrderRepository.java
└── domain/
    ├── User.java
    └── Order.java
```

**장점**: 레이어별 역할 명확, 소규모 프로젝트에 적합

### 설정 파일 관리

#### application.yml 구조
```yaml
spring:
  profiles:
    active: dev  # 또는 prod

---
# 개발 환경
spring:
  config:
    activate:
      on-profile: dev
  datasource:
    url: jdbc:postgresql://localhost:5432/devdb
    username: devuser
    password: ${DB_PASSWORD}

---
# 프로덕션 환경
spring:
  config:
    activate:
      on-profile: prod
  datasource:
    url: ${DATABASE_URL}
```

### 네이밍 규칙 (Java/Spring)

#### 클래스
- **Entity**: `User`, `Order`, `Product`
- **DTO**: `UserCreateDto`, `UserResponseDto`
- **Controller**: `UserController`, `OrderController`
- **Service**: `UserService`, `OrderService`
- **Repository**: `UserRepository`, `OrderRepository`
- **Exception**: `UserNotFoundException`, `InvalidRequestException`

#### 메서드
- **조회**: `findById()`, `findAll()`, `getUser()`
- **생성**: `create()`, `save()`, `register()`
- **수정**: `update()`, `modify()`
- **삭제**: `delete()`, `remove()`

### 테스트 구조

```
test/java/com/example/project/
├── controller/
│   └── UserControllerTest.java          # @WebMvcTest
├── service/
│   └── UserServiceTest.java             # @ExtendWith(MockitoExtension.class)
├── repository/
│   └── UserRepositoryTest.java          # @DataJpaTest
└── integration/
    └── UserIntegrationTest.java         # @SpringBootTest
```

### 빌드 도구

#### Gradle (build.gradle)
```gradle
plugins {
    id 'java'
    id 'org.springframework.boot' version '3.2.0'
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
}
```

#### Maven (pom.xml)
```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
</dependencies>
```

---

## 모노레포 구조

프론트엔드와 백엔드를 하나의 레포지토리로 관리하는 경우:

```
monorepo/
├── .claude/                    # 공통 Claude 설정
│   ├── CLAUDE.md
│   └── docs/
├── frontend/                   # 프론트엔드 프로젝트
│   ├── src/
│   ├── package.json
│   └── README.md
├── backend/                    # Spring Boot 프로젝트
│   ├── src/
│   ├── build.gradle
│   └── README.md
├── shared/                     # 공통 코드 (타입, 상수 등)
├── docs/                       # 통합 문서
├── scripts/                    # 공통 스크립트
└── README.md                   # 루트 README
```

### 모노레포 도구
- **Turborepo**: 빠른 빌드 캐싱
- **Nx**: 강력한 모노레포 관리
- **Lerna**: 패키지 버전 관리

## 체크리스트

새로운 파일/디렉토리 추가 시:
- [ ] 적절한 위치에 배치되었는가?
- [ ] 네이밍 규칙을 따르는가?
- [ ] 관련 문서가 업데이트되었는가?
- [ ] 불필요한 depth가 없는가?
- [ ] 다른 개발자가 쉽게 찾을 수 있는가?

## 참고
- [코드 스타일 가이드](./code-style.md)
- [네이밍 규칙](./naming-conventions.md)
- [파일/폴더 구조 규칙](./file-structure.md)
