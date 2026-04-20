# 코드 스타일 가이드

> 프로젝트의 일관된 코드 스타일을 유지하기 위한 가이드입니다.

## 목차
- [일반 원칙](#일반-원칙)
- [TypeScript/JavaScript](#typescriptjavascript)
- [Java/Spring Boot](#javaspring-boot)
- [포맷팅 규칙](#포맷팅-규칙)
- [주석 및 문서화](#주석-및-문서화)
- [자동화 도구](#자동화-도구)

---

## 일반 원칙

### 1. 읽기 쉬운 코드
코드는 작성하는 시간보다 읽는 시간이 더 많습니다.

```typescript
// [금지] 나쁜 예 - 이해하기 어려움
const x = u.filter(x => x.a > 18).map(x => x.n);

// [권장] 좋은 예 - 명확함
const adultUserNames = users
  .filter(user => user.age > 18)
  .map(user => user.name);
```

### 2. 일관성
프로젝트 전체에서 동일한 스타일을 유지합니다.

```typescript
// 한 파일에서는 화살표 함수, 다른 파일에서는 function 선언 [금지]
// 프로젝트 전체에서 하나의 스타일로 통일 [권장]
```

### 3. 단순함
복잡한 로직보다 단순하고 명확한 코드를 선호합니다.

```typescript
// [금지] 나쁜 예 - 과도하게 복잡
const result = data.reduce((acc, item) =>
  item.type === 'A' ? [...acc, { ...item, processed: true }] : acc, []
);

// [권장] 좋은 예 - 명확함
const typeAItems = data.filter(item => item.type === 'A');
const processedItems = typeAItems.map(item => ({
  ...item,
  processed: true
}));
```

### 4. DRY (Don't Repeat Yourself)
중복 코드를 제거하고 재사용 가능한 함수/컴포넌트로 분리합니다.

```typescript
// [금지] 나쁜 예 - 중복
function getUserEmail() {
  return user.email?.toLowerCase().trim();
}
function getAdminEmail() {
  return admin.email?.toLowerCase().trim();
}

// [권장] 좋은 예 - 재사용
function normalizeEmail(email?: string) {
  return email?.toLowerCase().trim();
}
```

---

## TypeScript/JavaScript

### 네이밍 규칙

#### 변수/함수: camelCase
```typescript
const userName = 'John';
const isActive = true;
function getUserById(id: string) { }
```

#### 클래스/인터페이스/타입: PascalCase
```typescript
class UserService { }
interface UserData { }
type UserRole = 'admin' | 'user';
```

#### 상수: UPPER_SNAKE_CASE
```typescript
const MAX_RETRY_COUNT = 3;
const API_BASE_URL = 'https://api.example.com';
```

#### Private 멤버: _(언더스코어) 접두사
```typescript
class UserService {
  private _cache: Map<string, User>;

  private _fetchFromCache(id: string) { }
}
```

### 타입 사용

#### 명시적 타입 선언
```typescript
// [금지] 나쁜 예
const users = [];
function getUser(id) { }

// [권장] 좋은 예
const users: User[] = [];
function getUser(id: string): User | null { }
```

#### 타입 vs 인터페이스
```typescript
// 객체 구조 정의 - interface 사용 (확장 가능)
interface User {
  id: string;
  name: string;
}

interface Admin extends User {
  permissions: string[];
}

// 유니온, 인터섹션, 유틸리티 타입 - type 사용
type UserRole = 'admin' | 'user' | 'guest';
type PartialUser = Partial<User>;
type ApiResponse<T> = {
  data: T;
  error?: string;
};
```

#### any 사용 지양
```typescript
// [금지] 나쁜 예
function processData(data: any) { }

// [권장] 좋은 예
function processData<T>(data: T) { }
// 또는
function processData(data: unknown) { }
```

### 함수 작성

#### 화살표 함수 vs 일반 함수
```typescript
// 일반 함수 - 메서드, 생성자, this 필요시
class UserService {
  getUser(id: string) {
    return this.users.find(u => u.id === id);
  }
}

// 화살표 함수 - 콜백, 간단한 함수
const numbers = [1, 2, 3];
const doubled = numbers.map(n => n * 2);

// 독립 함수 - export하는 유틸리티
export function formatDate(date: Date): string {
  return date.toISOString();
}
```

#### 단일 책임 원칙
```typescript
// [금지] 나쁜 예 - 여러 책임
function saveUserAndSendEmail(user: User) {
  database.save(user);
  emailService.send(user.email, 'Welcome!');
  analytics.track('user_created');
}

// [권장] 좋은 예 - 각각 분리
function saveUser(user: User) {
  return database.save(user);
}

function sendWelcomeEmail(user: User) {
  return emailService.send(user.email, 'Welcome!');
}

function trackUserCreation() {
  analytics.track('user_created');
}

// 조합
async function registerUser(user: User) {
  const savedUser = await saveUser(user);
  await sendWelcomeEmail(savedUser);
  trackUserCreation();
  return savedUser;
}
```

#### 매개변수 개수 제한
```typescript
// [금지] 나쁜 예 - 매개변수 너무 많음
function createUser(
  name: string,
  email: string,
  age: number,
  address: string,
  phone: string
) { }

// [권장] 좋은 예 - 객체로 그룹화
interface CreateUserParams {
  name: string;
  email: string;
  age: number;
  address: string;
  phone: string;
}

function createUser(params: CreateUserParams) { }
```

### 비동기 처리

#### async/await 사용
```typescript
// [금지] 나쁜 예 - Promise 체이닝
function getUser(id: string) {
  return fetch(`/api/users/${id}`)
    .then(res => res.json())
    .then(data => data.user)
    .catch(err => console.error(err));
}

// [권장] 좋은 예 - async/await
async function getUser(id: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${id}`);
    const data = await response.json();
    return data.user;
  } catch (error) {
    console.error('Failed to fetch user:', error);
    throw error;
  }
}
```

#### 에러 처리
```typescript
// [권장] 명시적 에러 처리
async function fetchUserData(id: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${id}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof NetworkError) {
      // 네트워크 에러 처리
    } else if (error instanceof ValidationError) {
      // 검증 에러 처리
    }
    throw error;
  }
}
```

### 객체 및 배열

#### 구조 분해 할당
```typescript
// [권장] 좋은 예
const { name, email } = user;
const [first, second, ...rest] = items;

// 함수 매개변수에서도 사용
function displayUser({ name, email }: User) {
  console.log(`${name} (${email})`);
}
```

#### 스프레드 연산자
```typescript
// 객체 복사 및 병합
const updatedUser = { ...user, name: 'New Name' };

// 배열 복사 및 병합
const allItems = [...items1, ...items2];
```

#### 옵셔널 체이닝
```typescript
// [권장] 좋은 예
const city = user?.address?.city;
const firstItem = items?.[0];
const result = fetchData?.();
```

---

## Java/Spring Boot

### 네이밍 규칙

#### 클래스: PascalCase
```java
public class UserService { }
public class OrderController { }
```

#### 메서드/변수: camelCase
```java
private String userName;
public User findUserById(Long id) { }
```

#### 상수: UPPER_SNAKE_CASE
```java
public static final int MAX_RETRY_COUNT = 3;
private static final String API_BASE_URL = "https://api.example.com";
```

#### 패키지: 소문자, 점(.) 구분
```java
package com.example.project.user.service;
```

### 클래스 구조

#### 표준 순서
```java
public class UserService {
    // 1. Static 상수
    private static final Logger log = LoggerFactory.getLogger(UserService.class);

    // 2. Instance 필드
    private final UserRepository userRepository;
    private final EmailService emailService;

    // 3. 생성자
    public UserService(UserRepository userRepository, EmailService emailService) {
        this.userRepository = userRepository;
        this.emailService = emailService;
    }

    // 4. Public 메서드
    public User createUser(UserCreateDto dto) {
        // ...
    }

    // 5. Private 메서드
    private void validateUser(User user) {
        // ...
    }
}
```

### 의존성 주입

#### 생성자 주입 (권장)
```java
// [권장] 좋은 예 - 생성자 주입
@Service
@RequiredArgsConstructor  // Lombok
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;
}

// 또는
@Service
public class UserService {
    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
}
```

#### 필드 주입 지양
```java
// [금지] 나쁜 예 - 필드 주입
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;  // 지양
}
```

### 메서드 작성

#### 명확한 이름
```java
// [금지] 나쁜 예
public User get(Long id) { }
public void do() { }

// [권장] 좋은 예
public User findById(Long id) { }
public Optional<User> findByEmail(String email) { }
public void deleteUser(Long id) { }
```

#### 반환 타입
```java
// null 반환 지양 - Optional 사용
public Optional<User> findById(Long id) {
    return userRepository.findById(id);
}

// 컬렉션은 빈 컬렉션 반환
public List<User> findAll() {
    List<User> users = userRepository.findAll();
    return users != null ? users : Collections.emptyList();
}
```

### 예외 처리

```java
// 명시적 예외 처리
@Transactional
public User createUser(UserCreateDto dto) {
    validateUserDto(dto);

    if (userRepository.existsByEmail(dto.getEmail())) {
        throw new DuplicateEmailException("Email already exists");
    }

    User user = dto.toEntity();
    return userRepository.save(user);
}

// 커스텀 예외
public class DuplicateEmailException extends RuntimeException {
    public DuplicateEmailException(String message) {
        super(message);
    }
}
```

### 레이어 구조

#### Controller
```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;

    @GetMapping("/{id}")
    public ResponseEntity<UserResponseDto> getUser(@PathVariable Long id) {
        User user = userService.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
        return ResponseEntity.ok(UserResponseDto.from(user));
    }

    @PostMapping
    public ResponseEntity<UserResponseDto> createUser(
        @Valid @RequestBody UserCreateDto dto
    ) {
        User user = userService.createUser(dto);
        return ResponseEntity.status(HttpStatus.CREATED)
            .body(UserResponseDto.from(user));
    }
}
```

#### Service
```java
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;

    public Optional<User> findById(Long id) {
        return userRepository.findById(id);
    }

    @Transactional
    public User createUser(UserCreateDto dto) {
        // 비즈니스 로직
        User user = dto.toEntity();
        return userRepository.save(user);
    }
}
```

#### Repository
```java
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);

    @Query("SELECT u FROM User u WHERE u.active = true")
    List<User> findActiveUsers();
}
```

---

## 포맷팅 규칙

### 들여쓰기
- **스페이스 2칸** (TypeScript/JavaScript)
- **스페이스 4칸** (Java)
- 탭 사용 지양

### 줄 길이
- **최대 100자** (권장)
- 120자 초과 시 줄바꿈

### 줄바꿈
```typescript
// 함수 매개변수
function createUser(
  name: string,
  email: string,
  age: number
): User {
  // ...
}

// 객체
const user = {
  name: 'John',
  email: 'john@example.com',
  address: {
    city: 'Seoul',
    country: 'Korea'
  }
};

// 메서드 체이닝
const result = items
  .filter(item => item.active)
  .map(item => item.name)
  .sort();
```

### 공백
```typescript
// 연산자 주변
const sum = a + b;
const isValid = x > 10 && y < 20;

// 함수 매개변수
function add(a: number, b: number) { }

// 객체
const user = { name: 'John', age: 30 };

// 배열
const numbers = [1, 2, 3, 4];
```

### 세미콜론
```typescript
// TypeScript/JavaScript: 세미콜론 사용 (권장)
const name = 'John';
const age = 30;

// 또는 일관되게 생략 (팀 규칙 따름)
```

---

## 주석 및 문서화

### 주석 작성 원칙

#### 1. Why, not What
```typescript
// [금지] 나쁜 예 - What (코드만 봐도 알 수 있음)
// 사용자 이름을 대문자로 변환
const upperName = user.name.toUpperCase();

// [권장] 좋은 예 - Why (이유 설명)
// DB는 이름을 대문자로 저장하므로 비교 전 변환 필요
const upperName = user.name.toUpperCase();
```

#### 2. 복잡한 로직 설명
```typescript
// [권장] 좋은 예
// 사용자가 마지막 로그인 후 30일 이상 지났고,
// 프리미엄 구독이 없으면 계정 비활성화
if (daysSinceLastLogin > 30 && !user.isPremium) {
  deactivateAccount(user);
}
```

#### 3. TODO/FIXME
```typescript
// TODO: 성능 최적화 필요 - 캐싱 구현 예정
// FIXME: 엣지 케이스 처리 필요 (이메일이 null인 경우)
// HACK: 임시 해결책 - 리팩토링 필요
```

### JSDoc/JavaDoc

#### TypeScript/JavaScript
```typescript
/**
 * 사용자를 ID로 조회합니다.
 *
 * @param id - 사용자 ID
 * @returns 사용자 객체 또는 null
 * @throws {UserNotFoundException} 사용자를 찾을 수 없을 때
 *
 * @example
 * ```ts
 * const user = await getUser('123');
 * ```
 */
async function getUser(id: string): Promise<User | null> {
  // ...
}
```

#### Java
```java
/**
 * 사용자를 생성합니다.
 *
 * @param dto 사용자 생성 DTO
 * @return 생성된 사용자
 * @throws DuplicateEmailException 이메일이 이미 존재할 때
 */
@Transactional
public User createUser(UserCreateDto dto) {
    // ...
}
```

---

## 자동화 도구

### ESLint (TypeScript/JavaScript)
```json
// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended"
  ],
  "rules": {
    "no-console": "warn",
    "no-unused-vars": "error",
    "@typescript-eslint/no-explicit-any": "error"
  }
}
```

### Prettier
```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "printWidth": 100,
  "trailingComma": "es5"
}
```

### CheckStyle (Java)
```xml
<!-- checkstyle.xml -->
<module name="Checker">
  <module name="LineLength">
    <property name="max" value="120"/>
  </module>
  <module name="Indentation">
    <property name="basicOffset" value="4"/>
  </module>
</module>
```

### Spotless (Java)
```gradle
// build.gradle
spotless {
    java {
        googleJavaFormat()
        importOrder()
        removeUnusedImports()
    }
}
```

### Pre-commit Hook
```bash
# .husky/pre-commit
#!/bin/sh
npm run lint
npm run format:check
npm run type-check
```

---

## 체크리스트

### 코드 작성 시
- [ ] 네이밍 규칙 준수
- [ ] 타입 명시 (TypeScript)
- [ ] 단일 책임 원칙
- [ ] DRY 원칙
- [ ] 에러 처리
- [ ] 주석 (필요시 Why 설명)

### 커밋 전
- [ ] ESLint/CheckStyle 통과
- [ ] Prettier 포맷팅 적용
- [ ] 불필요한 주석 제거
- [ ] Console.log 제거
- [ ] 테스트 통과

---

## 참고
- [네이밍 규칙](./naming-conventions.md)
- [파일/폴더 구조 규칙](./file-structure.md)
- [주석 및 문서화 규칙](./documentation-rules.md)
- [TypeScript 컨벤션](./ts-js-conventions.md)
