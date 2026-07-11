# Database Documentation

## Overview

The Online Examination Slot Booking System uses **MySQL** as the primary relational database. Django ORM is used to interact with the database, providing secure and efficient CRUD operations.

---

## Database Technology

- Database: MySQL
- ORM: Django ORM
- Migration Tool: Django Migrations

---

## Main Modules

The database is organized into the following functional modules:

- Accounts
- Academics
- Examinations
- Payments
- Notifications

---

## Main Entities

### Student

Stores student information.

Typical attributes include:

- Student ID
- Name
- Email
- Password
- Department
- Semester

---

### Faculty

Stores faculty information.

Typical attributes include:

- Faculty ID
- Name
- Email
- Department

---

### Examination Slot

Stores available examination slots.

Typical attributes include:

- Slot ID
- Date
- Time
- Subject
- Capacity

---

### Slot Booking

Stores examination bookings made by students.

Typical attributes include:

- Booking ID
- Student
- Examination Slot
- Booking Status

---

### Hall Ticket

Stores generated hall tickets.

Typical attributes include:

- Hall Ticket Number
- Student
- Examination
- Seat Number

---

### Payment

Stores payment details.

Typical attributes include:

- Payment ID
- Student
- Amount
- Payment Status
- Transaction Date

---

### Result

Stores examination results.

Typical attributes include:

- Result ID
- Student
- Subject
- Marks
- Grade

---

### Notification

Stores notifications sent to users.

Typical attributes include:

- Notification ID
- Title
- Message
- Created Date

---

## Relationships

- One Student can book multiple Examination Slots.
- One Examination Slot can have multiple Bookings.
- Each Booking belongs to one Student.
- Each Booking belongs to one Examination Slot.
- Each Student can have one or more Payments.
- Each Student receives Hall Tickets.
- Faculty members manage examinations and publish results.

---

## Security

The application uses:

- Django ORM
- CSRF Protection
- Authentication & Authorization
- Environment Variables
- Session Management

These features help protect the application from common web security threats.