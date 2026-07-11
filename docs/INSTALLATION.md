# Installation Guide

This guide explains how to set up and run the Online Examination Slot Booking System on your local machine.

---

## Prerequisites

Before running the project, ensure the following software is installed:

- Python 3.10 or later
- MySQL Server
- Git
- Visual Studio Code (recommended)

---

## Clone the Repository

```bash
git clone https://github.com/chaitanyateja13/online-examination-slot-booking-system.git
```

Navigate into the project directory:

```bash
cd online-examination-slot-booking-system
```

---

## Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment (Windows):

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file using `.env.example` and configure your MySQL database credentials.

---

## Apply Database Migrations

```bash
python manage.py migrate
```

---

## Run the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

## Project Modules

- Student Management
- Faculty Management
- Examination Slot Booking
- Hall Ticket Generation
- Payment Management
- Results Management
- Notifications

---

## Troubleshooting

- Ensure MySQL is running before starting the application.
- Verify that all required packages are installed.
- Check your `.env` file for correct database configuration.