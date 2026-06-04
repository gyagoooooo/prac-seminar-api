# Seminar Room Reservation API

Flask, MariaDB, Docker, GitHub Actions를 활용하여 구현한 세미나룸 예약 관리 API입니다.

## 프로젝트 개요

세미나룸 정보와 예약 정보를 관리할 수 있는 REST API를 제공하며, Docker Compose를 이용하여 API 서버와 MariaDB를 컨테이너 환경에서 실행할 수 있습니다.

또한 Git 브랜치 전략(devA, devB, main)을 적용하고 GitHub Actions를 활용하여 CI 환경을 구성하였습니다.

---

## 기술 스택

### Backend

* Python 3.12
* Flask
* Gunicorn

### Database

* MariaDB 10.6
* PyMySQL

### Infrastructure

* Docker
* Docker Compose
* GitHub Actions

---

## 프로젝트 구조

```text
seminar-api/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── db.py
│   ├── routes.py
│
├── migrations/
│   └── 001_init.sql
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   └── index.html
│
├── tests/
│   └── test_api.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── wsgi.py
└── README.md
```

---

## 브랜치 전략

```text
main  : 배포 브랜치
devA  : API 및 DB 개발
devB  : Docker 및 CI/CD 개발
```

작업 후 Pull Request를 통해 main 브랜치로 병합하는 방식으로 운영합니다.

---

## 데이터베이스 구조

### rooms

```sql
CREATE TABLE rooms (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  capacity INT NOT NULL,
  equipment VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP
);
```

### reservations

```sql
CREATE TABLE reservations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  room_id INT NOT NULL,
  user_name VARCHAR(100) NOT NULL,
  user_email VARCHAR(100) NOT NULL,
  date DATE NOT NULL,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  purpose VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_reservations_room
    FOREIGN KEY (room_id)
    REFERENCES rooms(id)
    ON DELETE CASCADE
);
```

---

## Docker Volume 영속화

MariaDB 데이터는 Docker Volume을 사용하여 관리합니다.

```yaml
volumes:
  seminar_data:
```

```yaml
db:
  volumes:
    - seminar_data:/var/lib/mysql
```

컨테이너를 재생성하더라도 데이터가 유지됩니다.

---

## 실행 방법

### 1. 저장소 클론

```bash
git clone https://github.com/gyagoooooo/prac-seminar-api.git
cd prac-seminar-api
```

### 2. Docker Compose 실행

```bash
docker compose up -d --build
```

### 3. 상태 확인

```bash
docker ps
```

예시

```text
seminar_api
seminar_db
```

---

## Health Check

```http
GET /health
```

응답

```json
{
  "status": "ok"
}
```

---

## API 명세

### 세미나룸 조회

```http
GET /api/rooms
```

응답

```json
{
  "items": [],
  "count": 0
}
```

---

### 세미나룸 단건 조회

```http
GET /api/rooms/{id}
```

---

### 세미나룸 생성

```http
POST /api/rooms
```

요청

```json
{
  "name": "세미나실 A",
  "capacity": 20,
  "equipment": "빔프로젝터"
}
```

응답

```json
{
  "id": 1,
  "message": "created"
}
```

---

### 세미나룸 수정

```http
PUT /api/rooms/{id}
```

---

### 세미나룸 삭제

```http
DELETE /api/rooms/{id}
```

---

### 예약 목록 조회

```http
GET /api/reservations
```

---

### 예약 필터 조회

```http
GET /api/reservations?room_id=1&date=2026-06-04
```

---

### 예약 생성

```http
POST /api/reservations
```

요청

```json
{
  "room_id": 1,
  "user_name": "홍길동",
  "user_email": "hong@example.com",
  "date": "2026-06-04",
  "start_time": "10:00:00",
  "end_time": "11:00:00",
  "purpose": "프로젝트 회의"
}
```

응답

```json
{
  "id": 1,
  "message": "reserved"
}
```

---

### 예약 취소

```http
DELETE /api/reservations/{id}
```

응답

```json
{
  "id": 1,
  "message": "cancelled"
}
```

---

## 테스트

```bash
pytest
```

---

## GitHub Actions

GitHub Actions를 이용하여 Push 시 자동으로 테스트가 실행되도록 구성하였습니다.

```text
main push
↓
GitHub Actions
↓
pytest 실행
↓
성공 시 CI 통과
```

---

## 실행 화면

### 메인 화면

* 세미나룸 등록
* 세미나룸 목록 조회
* 예약 등록
* 예약 목록 조회
* 예약 필터 조회
* 예약 취소

모든 기능은 REST API와 연동되어 동작합니다.

---

## 개발 환경

* Windows 11
* WSL2 Ubuntu
* Docker Engine
* MariaDB 10.6
* Python 3.12
* Flask 3.0.3
* GitHub Actions
