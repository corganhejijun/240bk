set APP_NAME=anime

python manage.py makemigrations %APP_NAME%
python manage.py migrate
PAUSE