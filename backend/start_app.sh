echo "Run migrations"
python manage.py migrate

echo "Start server"
python3 -m gunicorn djangoTestStripe.wsgi:application -w 4 --bind 0.0.0.0:8000

