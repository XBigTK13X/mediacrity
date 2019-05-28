#! /bin/bash

set -e

echo "Migrating database"

cd web

source $MEDIACRITY_CONFIG

echo "Building migrations"

python3 manage.py makemigrations media

echo "Applying migrations"

python3 manage.py migrate

read -d '' CREATE_SUPER_USER << EOF
from django.contrib.auth import get_user_model;
User = get_user_model();
User.objects.create_superuser('$MEDIACRITY_ADMIN_USER', '', '$MEDIACRITY_ADMIN_PASSWORD')
EOF

echo "Quietly creating superadmin"

echo $CREATE_SUPER_USER | python3 manage.py shell > /dev/null 2>&1 && true

cd ..
