python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
django-admin startproject config .
python manage.py startapp accounts
python manage.py startapp academics
python manage.py startapp payments
python manage.py startapp exams
python manage.py startapp notifications
