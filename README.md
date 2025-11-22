instructions

if to run locally

in powershell

python -m venv venv


.\venv\Scripts\Activate.ps1



pip install -r requirements.txt



py manage.py makemigrations accounts appointments



python manage.py migrate




$env:EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
$env:EMAIL_HOST="smtp.gmail.com"
$env:EMAIL_PORT="587"
$env:EMAIL_USE_TLS = "1"
$env:EMAIL_HOST_USER="joojgaming7@gmail.com"
$env:EMAIL_HOST_PASSWORD="ofcxbpabxvcpbsvo"
$env:DEFAULT_FROM_EMAIL="joojgaming7@gmail.com"


in the top is for the function of SMTP using gmail



python manage.py runserver


current admin details

username = MrRoy
password = Andmtk@2029

if want to create a new admin first Create a normal patient user first
Promote to ADMIN in shell:
py manage.py shell
from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.get(username="")
u.role = "ADMIN"
u.is_staff = True
u.save()
