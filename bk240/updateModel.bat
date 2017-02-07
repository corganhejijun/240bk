set APP_NAME=Anime

python manage.py makemigrations %APP_NAME%
python manage.py migrate
PAUSE