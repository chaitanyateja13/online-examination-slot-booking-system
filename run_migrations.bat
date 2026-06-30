call venv\Scripts\activate
python scripts\create_db.py
python manage.py makemigrations accounts academics payments exams notifications
python manage.py migrate