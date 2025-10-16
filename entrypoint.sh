#!/bin/bash
set -e

cd /app/src

if ! python manage.py showmigrations auth | grep -q '\[X\]'; then
  echo "First run detected — applying migrations..."
  python manage.py migrate --noinput

  echo "Creating superuser..."
  python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
EOF
else
  echo "Migrations already applied, skipping setup."
fi

python manage.py collectstatic --noinput

exec gunicorn src.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
