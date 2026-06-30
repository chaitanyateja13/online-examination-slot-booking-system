import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User, Faculty

def run():
    print("Seeding Faculty members...")
    for i in range(2, 7):
        username = f"faculty{i}"
        employee_id = f"FAC100{i}"
        
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, email=f"{username}@ems.com", password="faculty123", role="FACULTY")
            Faculty.objects.create(user=user, employee_id=employee_id, department="Computer Science")
            print(f"Created {username} ({employee_id})")
            
    print("Done seeding Faculty members.")

if __name__ == '__main__':
    run()
