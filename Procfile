release: python manage.py migrate ; cp frontend/static/style.css build/static/css
web: daphne ohq.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker -v2