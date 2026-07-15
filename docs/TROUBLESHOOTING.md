# Troubleshooting Guide

## Server Not Starting

- Activate the virtual environment.
- Install project dependencies.
- Verify database configuration.

---

## Database Connection Failed

- Ensure MySQL is running.
- Check credentials in the `.env` file.

---

## Static Files Not Loading

Run:

```bash
python manage.py collectstatic
```

---

## Migration Errors

Run:

```bash
python manage.py migrate
```

---

## Login Issues

- Verify username and password.
- Ensure the user account exists.