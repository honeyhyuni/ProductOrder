# ProductOrder(제품 주문 API 프로젝트)

### :star: 프로젝트 목적 및 주요 기능

- Django, Django-rest-framework, Docker 의 능률 향상 목적입니다.
- REST API 를 사용한 유연한 상품, 주문 API 설계가 목적입니다.
- DRF 의 다양한 CBV 를 사용해보는것이 목적입니다.
- JWT Token 을 이용한 유저 인증(쿠키)
- 이메일 로그인, 비밀번호 정규화
- 쿠폰룰 DB, 쿠폰 발급 DB, 유저 쿠폰 DB 분기

<hr/>

### 🛠 Backend 개발 환경

| 기술스택 | 버전 |
| --- | --- |
| python | 3.10 |
| django | 4.1.5 |
| djangorestframework | 3.14 |
| djangorestframework-simplejwt | 5.2.2 |
| postgreSQL | 15.2 |
| Docker | ... |

<hr/>

### 👏 API URL

### 유저 관련

| 기능 | HTTP METHOD | URL |
| --- | --- | --- |
| 회원가입 | POST | /accounts/signup |
| 로그인 | POST | /accounts/login |
| 유저 토큰 확인 및 access 토큰 재발급 | GET | /accounts/login |
| 로그아웃 | POST | /accounts/logout |

### 제품 관련

| 기능 | HTTP METHOD | URL |
| --- | --- | --- |
| 제품 등록 | POST | /product |
| 제품 목록 조회 | GET | /product |
| 제품 상세 조회 | GET | /product/{pk} |
| 제품 수정 | PUT, PATCH | /product/{pk} |
| 제품 삭제 | DELETE | /product/{pk} |
| 카테고리 목록 조회 | GET | /category |
| 카테고리 추가 | POST | /category |
| 제품 확인 및 사용 가능한 쿠폰 확인 | GET | /product/{pk}/order |
| 제품 구매 | POST | /product/{pk}/order |
| 제품 좋아요 | POST | /product/{pk]/like |
| 제품 좋아요 취소 | DELETE | /product/{pk}/unlike |

### 쿠폰 관련

| 기능 | HTTP METHOD | URL |
| --- | --- | --- |
| 쿠폰 목록 조회 | GET | /coupon |
| 쿠폰 등록 | POST | /coupon |
| 쿠폰 룰 목록 조회 | GET | /coupon/coupon-rules |
| 유저 쿠폰 조회 | GET | /coupon/user |
| 유저 쿠폰 등록 | POST | /coupon/user |

### 주문 관련

| 기능 | HTTP METHOD | URL |
| --- | --- | --- |
| 주문 목록 조회 | GET | /order |
| 주문 상세 조회 | GET | /order/{pk} |

<hr/>

### :computer: ERD

![https://user-images.githubusercontent.com/97664784/224468964-8a869828-4259-4798-a1a2-bdda2677d6e5.jpg](https://user-images.githubusercontent.com/97664784/224468964-8a869828-4259-4798-a1a2-bdda2677d6e5.jpg)
