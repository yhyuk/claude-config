# 테스트 전략

> 프로젝트의 종합적인 테스트 전략 및 가이드라인입니다.

## 목차
- [테스트 철학](#테스트-철학)
- [테스트 피라미드](#테스트-피라미드)
- [테스트 유형](#테스트-유형)
- [TDD (Test-Driven Development)](#tdd-test-driven-development)
- [테스트 커버리지](#테스트-커버리지)
- [OMC 테스트 도구](#omc-테스트-도구)
- [모범 사례](#모범-사례)

---

## 테스트 철학

### 왜 테스트를 작성하는가?

1. **버그 조기 발견** - 프로덕션 배포 전 문제 발견
2. **리팩토링 자신감** - 안전하게 코드 개선
3. **문서화** - 코드 사용법 예시 제공
4. **설계 개선** - 테스트 가능한 코드 = 좋은 설계
5. **회귀 방지** - 기존 기능 보호

### 테스트 작성 원칙

#### 1. FIRST 원칙
- **Fast** (빠름) - 테스트는 빨리 실행되어야 함
- **Independent** (독립적) - 테스트 간 의존성 없음
- **Repeatable** (반복 가능) - 어떤 환경에서든 동일한 결과
- **Self-Validating** (자가 검증) - 성공/실패 자동 판단
- **Timely** (적시) - 프로덕션 코드 전/직후 작성

#### 2. AAA 패턴
```typescript
test('should create user with valid data', () => {
  // Arrange (준비) - 테스트 데이터 및 환경 설정
  const userData = {
    name: 'John Doe',
    email: 'john@example.com'
  };

  // Act (실행) - 테스트할 동작 수행
  const user = createUser(userData);

  // Assert (검증) - 결과 확인
  expect(user.name).toBe('John Doe');
  expect(user.email).toBe('john@example.com');
});
```

#### 3. Given-When-Then (BDD)
```typescript
describe('User authentication', () => {
  it('should return JWT token when login credentials are valid', () => {
    // Given (주어진 상황)
    const email = 'user@example.com';
    const password = 'password123';

    // When (특정 동작)
    const result = login(email, password);

    // Then (예상 결과)
    expect(result.token).toBeDefined();
    expect(result.expiresIn).toBe(3600);
  });
});
```

---

## 테스트 피라미드

```
        /\
       /  \      E2E Tests (10%)
      /    \     - 사용자 시나리오
     /------\    - UI 통합
    /        \
   /          \  Integration Tests (30%)
  /            \ - API 테스트
 /              \- DB 통합
/----------------\
  Unit Tests (60%)
  - 함수/메서드
  - 클래스 단위
```

### 비율 가이드
- **단위 테스트 (60%)** - 빠르고 많이
- **통합 테스트 (30%)** - 중요 흐름
- **E2E 테스트 (10%)** - 핵심 시나리오

---

## 테스트 유형

### 1. 단위 테스트 (Unit Tests)

**목적**: 개별 함수/메서드의 동작 검증

**특징**:
- 가장 빠름
- 격리된 환경
- Mock/Stub 사용

**예제 (TypeScript/Jest)**:
```typescript
// userService.test.ts
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with hashed password', () => {
      // Arrange
      const userData = {
        email: 'test@example.com',
        password: 'password123'
      };
      const hashSpy = jest.spyOn(bcrypt, 'hash')
        .mockResolvedValue('hashed_password');

      // Act
      const user = await userService.createUser(userData);

      // Assert
      expect(hashSpy).toHaveBeenCalledWith('password123', 10);
      expect(user.password).toBe('hashed_password');
    });

    it('should throw error when email already exists', async () => {
      // Arrange
      const existingEmail = 'existing@example.com';
      jest.spyOn(userRepository, 'findByEmail')
        .mockResolvedValue({ id: '1', email: existingEmail });

      // Act & Assert
      await expect(
        userService.createUser({ email: existingEmail, password: 'pw' })
      ).rejects.toThrow('Email already exists');
    });
  });
});
```

**예제 (Java/JUnit)**:
```java
// UserServiceTest.java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    @Mock
    private UserRepository userRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @InjectMocks
    private UserService userService;

    @Test
    void shouldCreateUserWithHashedPassword() {
        // Arrange
        UserCreateDto dto = new UserCreateDto("test@example.com", "password123");
        when(passwordEncoder.encode("password123")).thenReturn("hashed_password");
        when(userRepository.save(any(User.class))).thenAnswer(i -> i.getArgument(0));

        // Act
        User user = userService.createUser(dto);

        // Assert
        assertEquals("hashed_password", user.getPassword());
        verify(passwordEncoder).encode("password123");
        verify(userRepository).save(any(User.class));
    }

    @Test
    void shouldThrowExceptionWhenEmailExists() {
        // Arrange
        String existingEmail = "existing@example.com";
        when(userRepository.existsByEmail(existingEmail)).thenReturn(true);

        // Act & Assert
        assertThrows(DuplicateEmailException.class, () -> {
            userService.createUser(new UserCreateDto(existingEmail, "password"));
        });
    }
}
```

---

### 2. 통합 테스트 (Integration Tests)

**목적**: 여러 모듈/레이어 간 상호작용 검증

**특징**:
- 실제 DB/API 사용 (또는 테스트용)
- 단위 테스트보다 느림
- 실제 환경과 유사

**예제 (TypeScript/SuperTest)**:
```typescript
// userController.integration.test.ts
describe('User API Integration', () => {
  let app: Express;
  let testDb: Database;

  beforeAll(async () => {
    // 테스트 DB 설정
    testDb = await setupTestDatabase();
    app = createApp(testDb);
  });

  afterAll(async () => {
    await testDb.close();
  });

  describe('POST /api/users', () => {
    it('should create user and return 201', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          email: 'test@example.com',
          password: 'password123',
          name: 'Test User'
        })
        .expect(201);

      expect(response.body).toMatchObject({
        email: 'test@example.com',
        name: 'Test User'
      });
      expect(response.body.password).toBeUndefined(); // 비밀번호는 반환 안 됨

      // DB 검증
      const user = await testDb.users.findByEmail('test@example.com');
      expect(user).toBeDefined();
      expect(user.password).not.toBe('password123'); // 해시됨
    });

    it('should return 400 for invalid email', async () => {
      await request(app)
        .post('/api/users')
        .send({
          email: 'invalid-email',
          password: 'password123'
        })
        .expect(400);
    });
  });
});
```

**예제 (Java/Spring Boot)**:
```java
// UserControllerIntegrationTest.java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureTestDatabase
class UserControllerIntegrationTest {
    @Autowired
    private TestRestTemplate restTemplate;

    @Autowired
    private UserRepository userRepository;

    @BeforeEach
    void setUp() {
        userRepository.deleteAll();
    }

    @Test
    void shouldCreateUserAndReturn201() {
        // Arrange
        UserCreateDto dto = new UserCreateDto(
            "test@example.com",
            "password123",
            "Test User"
        );

        // Act
        ResponseEntity<UserResponseDto> response = restTemplate.postForEntity(
            "/api/users",
            dto,
            UserResponseDto.class
        );

        // Assert
        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("test@example.com", response.getBody().getEmail());

        // DB 검증
        Optional<User> savedUser = userRepository.findByEmail("test@example.com");
        assertTrue(savedUser.isPresent());
        assertNotEquals("password123", savedUser.get().getPassword()); // 해시됨
    }
}
```

---

### 3. E2E 테스트 (End-to-End Tests)

**목적**: 실제 사용자 시나리오 검증

**특징**:
- 전체 애플리케이션 테스트
- 브라우저 자동화 (Playwright, Cypress)
- 가장 느림

**예제 (Playwright)**:
```typescript
// user-registration.e2e.test.ts
import { test, expect } from '@playwright/test';

test.describe('User Registration Flow', () => {
  test('should complete full registration process', async ({ page }) => {
    // 1. 회원가입 페이지로 이동
    await page.goto('/register');

    // 2. 폼 작성
    await page.fill('input[name="email"]', 'newuser@example.com');
    await page.fill('input[name="password"]', 'SecurePassword123!');
    await page.fill('input[name="confirmPassword"]', 'SecurePassword123!');
    await page.fill('input[name="name"]', 'New User');

    // 3. 제출
    await page.click('button[type="submit"]');

    // 4. 성공 메시지 확인
    await expect(page.locator('.success-message')).toBeVisible();
    await expect(page.locator('.success-message')).toContainText(
      'Registration successful'
    );

    // 5. 자동 로그인 확인
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('.user-name')).toContainText('New User');
  });

  test('should show error for duplicate email', async ({ page }) => {
    // Arrange - 기존 사용자 생성
    await createTestUser('existing@example.com');

    // Act
    await page.goto('/register');
    await page.fill('input[name="email"]', 'existing@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    // Assert
    await expect(page.locator('.error-message')).toContainText(
      'Email already exists'
    );
  });
});
```

---

### 4. 스냅샷 테스트

**목적**: UI 컴포넌트 변경 감지

**예제 (React Testing Library)**:
```typescript
// UserCard.test.tsx
import { render } from '@testing-library/react';
import UserCard from './UserCard';

test('should match snapshot', () => {
  const user = {
    name: 'John Doe',
    email: 'john@example.com',
    avatar: 'https://example.com/avatar.jpg'
  };

  const { container } = render(<UserCard user={user} />);

  expect(container.firstChild).toMatchSnapshot();
});
```

---

## TDD (Test-Driven Development)

### TDD 사이클: Red-Green-Refactor

```
1. Red (실패)
   ↓
   테스트 작성 → 실행 → 실패 확인
   ↓
2. Green (성공)
   ↓
   최소 코드 작성 → 테스트 통과
   ↓
3. Refactor (리팩토링)
   ↓
   코드 개선 → 테스트 여전히 통과
   ↓
   반복
```

### OMC TDD 워크플로우

```bash
# TDD 모드 시작
/oh-my-claudecode:tdd
"Implement user authentication"
```

**자동 실행**:
1. 인터페이스 스캐폴딩
2. **테스트 먼저 작성**
3. 테스트 실행 (실패 확인)
4. 최소 구현 작성
5. 테스트 통과 확인
6. 리팩토링
7. 80%+ 커버리지 확인

### TDD 예제

#### 1단계: 테스트 먼저 작성 (Red)
```typescript
// calculator.test.ts
describe('Calculator', () => {
  test('should add two numbers', () => {
    const calculator = new Calculator();
    expect(calculator.add(2, 3)).toBe(5);
  });
});

// 실행 → 실패 (Calculator 클래스 없음)
```

#### 2단계: 최소 구현 (Green)
```typescript
// calculator.ts
class Calculator {
  add(a: number, b: number): number {
    return a + b;
  }
}

// 실행 → 성공
```

#### 3단계: 리팩토링 (Refactor)
```typescript
// calculator.ts
class Calculator {
  add(a: number, b: number): number {
    this.validateNumbers(a, b);
    return a + b;
  }

  private validateNumbers(...nums: number[]): void {
    if (nums.some(n => typeof n !== 'number')) {
      throw new TypeError('All arguments must be numbers');
    }
  }
}

// 테스트 여전히 통과
```

---

## 테스트 커버리지

### 목표 커버리지
- **전체**: 80% 이상
- **핵심 비즈니스 로직**: 90% 이상
- **유틸리티/헬퍼**: 70% 이상
- **UI 컴포넌트**: 60% 이상

### 커버리지 측정

**TypeScript/Jest**:
```bash
npm test -- --coverage

# 상세 보고서
npm test -- --coverage --coverageReporters=html
open coverage/index.html
```

**Java/JaCoCo**:
```gradle
// build.gradle
plugins {
    id 'jacoco'
}

jacoco {
    toolVersion = "0.8.10"
}

test {
    finalizedBy jacocoTestReport
}

jacocoTestReport {
    reports {
        xml.required = true
        html.required = true
    }
}
```

```bash
./gradlew test jacocoTestReport
open build/reports/jacoco/test/html/index.html
```

### 커버리지 타입

#### 1. Line Coverage (라인 커버리지)
실행된 코드 라인 비율

#### 2. Branch Coverage (분기 커버리지)
```typescript
function checkAge(age: number) {
  if (age >= 18) {  // 분기 1
    return 'adult';
  }
  return 'minor';   // 분기 2
}

// 100% 분기 커버리지를 위해 두 경로 모두 테스트
test('adult case', () => expect(checkAge(20)).toBe('adult'));
test('minor case', () => expect(checkAge(15)).toBe('minor'));
```

#### 3. Function Coverage (함수 커버리지)
호출된 함수 비율

#### 4. Statement Coverage (구문 커버리지)
실행된 구문 비율

---

## OMC 테스트 도구

### test-engineer 에이전트

```typescript
// 테스트 전략 수립
Task(
  subagent_type: "oh-my-claudecode:test-engineer",
  prompt: "Create comprehensive test strategy for authentication module"
)

// 테스트 커버리지 향상
Task(
  subagent_type: "oh-my-claudecode:test-engineer",
  prompt: "Improve test coverage to 80% for UserService"
)

// Flaky 테스트 수정
Task(
  subagent_type: "oh-my-claudecode:test-engineer",
  prompt: "Fix flaky tests in payment integration"
)
```

### TDD 워크플로우

```bash
/oh-my-claudecode:tdd
"Implement payment processing with Stripe"
```

**자동 실행**:
- 테스트 먼저 작성
- 최소 구현
- 리팩토링
- 커버리지 검증

### UltraQA 모드

```bash
# Autopilot에 자동 포함
/oh-my-claudecode:autopilot
"Build user management system"
```

**QA 사이클**:
1. Test → 실행
2. Verify → 검증
3. Fix → 실패 시 수정
4. Repeat → 성공까지 반복

---

## 모범 사례

### 1. 테스트 이름은 명확하게

```typescript
// ❌ 나쁜 예
test('user test', () => { });
test('should work', () => { });

// ✅ 좋은 예
test('should create user with valid email', () => { });
test('should throw error when email is duplicate', () => { });
test('should hash password before saving', () => { });
```

### 2. 하나의 테스트, 하나의 검증

```typescript
// ❌ 나쁜 예 - 여러 개념 테스트
test('user operations', () => {
  const user = createUser(data);
  expect(user.name).toBe('John');

  const updated = updateUser(user, { name: 'Jane' });
  expect(updated.name).toBe('Jane');

  deleteUser(user.id);
  expect(getUser(user.id)).toBeNull();
});

// ✅ 좋은 예 - 각각 분리
test('should create user with correct name', () => {
  const user = createUser({ name: 'John' });
  expect(user.name).toBe('John');
});

test('should update user name', () => {
  const user = createUser({ name: 'John' });
  const updated = updateUser(user, { name: 'Jane' });
  expect(updated.name).toBe('Jane');
});

test('should delete user', () => {
  const user = createUser({ name: 'John' });
  deleteUser(user.id);
  expect(getUser(user.id)).toBeNull();
});
```

### 3. 테스트 데이터는 명확하게

```typescript
// ❌ 나쁜 예 - 매직 넘버/문자열
test('should validate age', () => {
  expect(isAdult(18)).toBe(true);
  expect(isAdult(17)).toBe(false);
});

// ✅ 좋은 예 - 의미있는 상수
test('should validate age', () => {
  const ADULT_AGE = 18;
  const MINOR_AGE = 17;

  expect(isAdult(ADULT_AGE)).toBe(true);
  expect(isAdult(MINOR_AGE)).toBe(false);
});
```

### 4. 테스트는 독립적으로

```typescript
// ❌ 나쁜 예 - 테스트 간 의존성
let user;

test('create user', () => {
  user = createUser({ name: 'John' });
});

test('update user', () => {
  updateUser(user, { name: 'Jane' });  // 이전 테스트에 의존
});

// ✅ 좋은 예 - 각 테스트 독립적
test('create user', () => {
  const user = createUser({ name: 'John' });
  expect(user.name).toBe('John');
});

test('update user', () => {
  const user = createUser({ name: 'John' });
  const updated = updateUser(user, { name: 'Jane' });
  expect(updated.name).toBe('Jane');
});
```

### 5. 엣지 케이스 테스트

```typescript
describe('divide', () => {
  test('should divide two numbers', () => {
    expect(divide(10, 2)).toBe(5);
  });

  test('should handle zero dividend', () => {
    expect(divide(0, 5)).toBe(0);
  });

  test('should throw error for division by zero', () => {
    expect(() => divide(10, 0)).toThrow('Division by zero');
  });

  test('should handle negative numbers', () => {
    expect(divide(-10, 2)).toBe(-5);
    expect(divide(10, -2)).toBe(-5);
  });

  test('should handle decimal results', () => {
    expect(divide(10, 3)).toBeCloseTo(3.333, 3);
  });
});
```

---

## 테스트 구조

### 프론트엔드
```
src/
├── components/
│   ├── UserCard.tsx
│   └── UserCard.test.tsx
├── services/
│   ├── userService.ts
│   └── userService.test.ts
└── __tests__/
    ├── integration/
    │   └── userAPI.test.ts
    └── e2e/
        └── userRegistration.spec.ts
```

### 백엔드 (Spring Boot)
```
src/
├── main/java/com/example/
│   ├── service/
│   │   └── UserService.java
│   └── controller/
│       └── UserController.java
└── test/java/com/example/
    ├── service/
    │   └── UserServiceTest.java
    ├── controller/
    │   └── UserControllerTest.java
    └── integration/
        └── UserIntegrationTest.java
```

---

## 체크리스트

### 새 기능 개발 시
- [ ] TDD로 테스트 먼저 작성
- [ ] 단위 테스트 작성
- [ ] 통합 테스트 작성 (필요 시)
- [ ] E2E 테스트 작성 (핵심 흐름)
- [ ] 80% 이상 커버리지 달성
- [ ] 모든 테스트 통과

### PR 전
- [ ] 새 테스트 모두 통과
- [ ] 기존 테스트 깨지지 않음
- [ ] 커버리지 감소하지 않음
- [ ] Flaky 테스트 없음

---

## 참고
- [단위 테스트 가이드](./unit-testing.md)
- [통합 테스트 가이드](./integration-testing.md)
- [E2E 테스트 가이드](./e2e-testing.md)
- [테스트 커버리지 기준](./test-coverage.md)
- [OMC test-engineer](./omc/agents/domain-specialists.md)
- [OMC TDD 워크플로우](./omc/workflows/)
