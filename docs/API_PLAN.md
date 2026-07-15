# REST API Planning

## Overview

The current version of the Online Examination Slot Booking System follows Django's Model–View–Template (MVT) architecture. REST APIs are planned for future releases to support mobile applications and third-party integrations.

---

## Proposed Endpoints

### Authentication

- POST /api/login
- POST /api/logout

### Students

- GET /api/students/profile
- PUT /api/students/profile

### Examination Slots

- GET /api/exams/slots
- POST /api/exams/book-slot

### Hall Tickets

- GET /api/hall-ticket

### Payments

- POST /api/payments
- GET /api/payments/history

### Results

- GET /api/results

### Notifications

- GET /api/notifications

---

## Future Improvements

- JWT Authentication
- Rate Limiting
- API Versioning
- Swagger/OpenAPI Documentation