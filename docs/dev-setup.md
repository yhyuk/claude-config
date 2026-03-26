# 개발 환경 설정

> 로컬 개발 환경 구축 가이드입니다.

## 목차
- [프론트엔드 개발 환경](#프론트엔드-개발-환경)
- [백엔드 개발 환경](#백엔드-개발-환경)
- [공통 도구](#공통-도구)
- [통합 개발 환경](#통합-개발-환경)

---

## 프론트엔드 개발 환경

### 필수 요구사항

#### 1. Node.js
- **버전**: Node.js 18.x 이상 (LTS 권장)
- **설치**:
  ```bash
  # nvm 사용 (권장)
  nvm install 18
  nvm use 18

  # 또는 직접 다운로드
  # https://nodejs.org/
  ```

#### 2. 패키지 매니저
선택한 패키지 매니저 하나만 사용:

**npm** (Node.js 기본 포함)
```bash
npm --version
```

**yarn** (선택)
```bash
npm install -g yarn
```

**pnpm** (선택 - 디스크 공간 효율적)
```bash
npm install -g pnpm
```

**bun** (선택 - 매우 빠름)
```bash
curl -fsSL https://bun.sh/install | bash
```

### 프로젝트 설정

#### 1. 저장소 클론
```bash
git clone <repository-url>
cd <project-name>
```

#### 2. 의존성 설치
```bash
# npm
npm install

# yarn
yarn install

# pnpm
pnpm install

# bun
bun install
```

#### 3. 환경 변수 설정
```bash
# .env.example을 복사
cp .env.example .env.local

# .env.local 파일 편집
# 필요한 환경 변수 값 입력
```

**.env.local 예시**:
```env
# API 엔드포인트
NEXT_PUBLIC_API_URL=http://localhost:8080/api
VITE_API_URL=http://localhost:8080/api

# 기타 환경 변수
NEXT_PUBLIC_APP_ENV=development
```

#### 4. 개발 서버 실행
```bash
# npm
npm run dev

# yarn
yarn dev

# pnpm
pnpm dev

# bun
bun dev
```

기본 주소: `http://localhost:3000` (프레임워크에 따라 다름)

### 프론트엔드 도구

#### ESLint 설정
```bash
# ESLint 실행
npm run lint

# 자동 수정
npm run lint:fix
```

#### Prettier 설정
```bash
# 포맷팅 확인
npm run format:check

# 포맷팅 적용
npm run format
```

#### TypeScript 타입 체크
```bash
npm run type-check
```

---

## 백엔드 개발 환경

### 필수 요구사항

#### 1. Java JDK
- **버전**: Java 17 이상 (LTS 권장)
- **설치**:
  ```bash
  # macOS (Homebrew)
  brew install openjdk@17

  # Ubuntu/Debian
  sudo apt install openjdk-17-jdk

  # Windows
  # https://adoptium.net/ 에서 다운로드
  ```

- **버전 확인**:
  ```bash
  java -version
  javac -version
  ```

#### 2. 빌드 도구

**Gradle** (권장)
```bash
# macOS
brew install gradle

# 또는 프로젝트에 포함된 Gradle Wrapper 사용
./gradlew --version
```

**Maven** (선택)
```bash
# macOS
brew install maven

# 또는 프로젝트에 포함된 Maven Wrapper 사용
./mvnw --version
```

#### 3. 데이터베이스

**PostgreSQL**
```bash
# macOS
brew install postgresql@15
brew services start postgresql@15

# Ubuntu/Debian
sudo apt install postgresql-15
sudo systemctl start postgresql

# Docker 사용 (권장)
docker run -d \
  --name postgres-dev \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=devdb \
  -p 5432:5432 \
  postgres:15
```

**MySQL** (선택)
```bash
# Docker
docker run -d \
  --name mysql-dev \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=devdb \
  -p 3306:3306 \
  mysql:8
```

### 프로젝트 설정

#### 1. 저장소 클론
```bash
git clone <repository-url>
cd <project-name>
```

#### 2. 환경 변수 설정

**application-dev.yml** (또는 .env)
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/devdb
    username: postgres
    password: postgres
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
```

또는 환경 변수로:
```bash
export DB_URL=jdbc:postgresql://localhost:5432/devdb
export DB_USERNAME=postgres
export DB_PASSWORD=postgres
```

#### 3. 빌드 및 실행

**Gradle**
```bash
# 빌드
./gradlew build

# 테스트 제외 빌드
./gradlew build -x test

# 실행
./gradlew bootRun

# 또는
java -jar build/libs/application.jar
```

**Maven**
```bash
# 빌드
./mvnw clean package

# 실행
./mvnw spring-boot:run

# 또는
java -jar target/application.jar
```

기본 주소: `http://localhost:8080`

#### 4. 데이터베이스 마이그레이션

**Flyway 사용 시**
```bash
./gradlew flywayMigrate
```

**Liquibase 사용 시**
```bash
./gradlew update
```

### 백엔드 도구

#### 코드 포맷팅
```bash
# Spotless (Gradle)
./gradlew spotlessApply

# CheckStyle
./gradlew checkstyleMain
```

#### 테스트 실행
```bash
# 전체 테스트
./gradlew test

# 특정 테스트
./gradlew test --tests UserServiceTest

# 통합 테스트
./gradlew integrationTest
```

---

## 공통 도구

### 1. Git
```bash
git --version

# 설정
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 2. Docker (선택 - 권장)
```bash
# macOS
brew install --cask docker

# Ubuntu
sudo apt install docker.io docker-compose

# 버전 확인
docker --version
docker-compose --version
```

**개발 환경 전체 실행 (docker-compose)**:
```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: devdb
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    ports:
      - "8080:8080"
    depends_on:
      - postgres

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
```

```bash
# 실행
docker-compose up -d

# 중지
docker-compose down
```

### 3. IDE / 에디터

#### VS Code (권장 - 프론트엔드)
**필수 확장**:
- ESLint
- Prettier
- TypeScript and JavaScript Language Features
- Auto Import
- Path Intellisense

**선택 확장**:
- Tailwind CSS IntelliSense
- GitLens
- Error Lens

**설정** (.vscode/settings.json):
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.updateImportsOnFileMove.enabled": "always"
}
```

#### IntelliJ IDEA (권장 - 백엔드)
**필수 플러그인**:
- Lombok
- Spring Boot
- Database Navigator

**설정**:
- Enable annotation processing (Lombok 사용 시)
- Code style: Google Java Style (또는 프로젝트 규칙)

### 4. API 테스트 도구

**Postman** (GUI)
- 다운로드: https://www.postman.com/downloads/

**HTTPie** (CLI - 권장)
```bash
# macOS
brew install httpie

# 사용
http GET http://localhost:8080/api/users
```

**curl** (기본 포함)
```bash
curl -X GET http://localhost:8080/api/users
```

---

## 통합 개발 환경

### 모노레포 전체 실행

#### 1. 루트에서 전체 설정
```bash
# 프론트엔드 의존성 설치
cd frontend && npm install && cd ..

# 백엔드 빌드
cd backend && ./gradlew build && cd ..
```

#### 2. 동시 실행 (concurrently 사용)
```json
// package.json (루트)
{
  "scripts": {
    "dev": "concurrently \"npm run dev:frontend\" \"npm run dev:backend\"",
    "dev:frontend": "cd frontend && npm run dev",
    "dev:backend": "cd backend && ./gradlew bootRun"
  },
  "devDependencies": {
    "concurrently": "^8.0.0"
  }
}
```

```bash
npm run dev
```

### 환경별 설정

#### 개발 (Development)
- 디버그 로그 활성화
- Hot reload 활성화
- Mock 데이터 사용 가능

#### 스테이징 (Staging)
- 프로덕션과 유사한 환경
- 실제 데이터베이스 연결
- 성능 모니터링

#### 프로덕션 (Production)
- 최적화된 빌드
- 에러 로그만 활성화
- HTTPS 필수

---

## 트러블슈팅

### 프론트엔드

#### 포트 이미 사용 중
```bash
# 프로세스 찾기 (macOS/Linux)
lsof -i :3000

# 프로세스 종료
kill -9 <PID>

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

#### 의존성 충돌
```bash
# node_modules 삭제 후 재설치
rm -rf node_modules package-lock.json
npm install
```

#### 캐시 문제
```bash
# npm 캐시 삭제
npm cache clean --force

# Next.js 캐시 삭제
rm -rf .next
```

### 백엔드

#### 데이터베이스 연결 실패
1. 데이터베이스 실행 확인
2. 포트 확인 (PostgreSQL: 5432, MySQL: 3306)
3. 연결 정보 확인 (URL, username, password)

#### 빌드 실패
```bash
# Gradle 캐시 삭제
./gradlew clean

# 의존성 재다운로드
./gradlew build --refresh-dependencies
```

#### 포트 충돌
```bash
# application.yml에서 포트 변경
server:
  port: 8081
```

---

## 체크리스트

### 초기 설정 완료 확인
- [ ] Node.js/Java 설치 및 버전 확인
- [ ] 패키지 매니저 설치
- [ ] Git 설정 완료
- [ ] IDE/에디터 설정 완료
- [ ] 데이터베이스 설치 및 실행
- [ ] 환경 변수 설정 (.env 파일)
- [ ] 프론트엔드 개발 서버 실행 확인
- [ ] 백엔드 서버 실행 확인
- [ ] API 통신 확인
- [ ] 테스트 실행 확인

### 일일 개발 시작 전
- [ ] Git pull (최신 코드 반영)
- [ ] 의존성 업데이트 확인
- [ ] 데이터베이스 실행 확인
- [ ] 개발 서버 실행

---

## 참고
- [프로젝트 구조](./project-structure.md)
- [기술 스택](./tech-stack.md)
- [Git 워크플로우](./git-workflow.md)
- [트러블슈팅 가이드](./troubleshooting.md)
