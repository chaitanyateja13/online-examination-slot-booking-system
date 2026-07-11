# Deployment Guide

## Overview

This document explains how the Online Examination Slot Booking System can be deployed in different environments.

---

# Deployment Requirements

Before deployment, ensure the following software is available:

- Python 3.10+
- MySQL Server
- Git
- Virtual Environment
- Web Server (Nginx or Apache)
- WSGI Server (Gunicorn or Waitress)

---

# Environment Variables

Create a `.env` file and configure:

- SECRET_KEY
- DEBUG
- DATABASE_NAME
- DATABASE_USER
- DATABASE_PASSWORD
- DATABASE_HOST
- DATABASE_PORT

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Apply Database Migrations

```bash
python manage.py migrate
```

---

# Collect Static Files

```bash
python manage.py collectstatic
```

---

# Run the Application

Development:

```bash
python manage.py runserver
```

Production:

Deploy using a WSGI server such as Gunicorn (Linux) or Waitress (Windows).

---

# Database Backup

Regular database backups are recommended.

Example:

- Daily backup
- Weekly backup
- Monthly archive

---

# Deployment Checklist

- Python Installed
- Virtual Environment Created
- Dependencies Installed
- Environment Variables Configured
- Database Migrated
- Static Files Collected
- Debug Disabled
- Secret Key Protected

---

# Future Deployment

The project can later be deployed on:

- AWS
- Microsoft Azure
- Google Cloud Platform
- DigitalOcean
- Railway
- Render

---

# Version Control

Always deploy from a stable Git branch.

Recommended:

- main
- release branches
