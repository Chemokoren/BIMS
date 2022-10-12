#!/usr/bin/env bash

set -e

# TODO: Set to URL of git repo.
PROJECT_GIT_URL='https://github.com/Chemokoren/BIMS.git'

PROJECT_BASE_PATH='/usr/local/apps/BIMS'

echo "Installing dependencies..."
apt-get update
apt-get install -y python3-dev python3-venv sqlite python-pip supervisor nginx git

# Create project directory
mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH

# Create virtual environment
mkdir -p $PROJECT_BASE_PATH/env
python3 -m venv $PROJECT_BASE_PATH/env

# Install python packages
$PROJECT_BASE_PATH/env/bin/pip install -r $PROJECT_BASE_PATH/requirements.txt
$PROJECT_BASE_PATH/env/bin/pip install uwsgi==2.0.20

# Run migrations and collectstatic
cd $PROJECT_BASE_PATH
$PROJECT_BASE_PATH/env/bin/python manage.py migrate
$PROJECT_BASE_PATH/env/bin/python manage.py collectstatic --noinput

# Configure supervisor
cp $PROJECT_BASE_PATH/deploy/supervisor_BIMS_api.conf /etc/supervisor/conf.d/BIMS_api.conf
supervisorctl reread
supervisorctl update
supervisorctl restart BIMS_api

# Configure nginx
cp $PROJECT_BASE_PATH/deploy/nginx_BIMS_api.conf /etc/nginx/sites-available/BIMS_api.conf
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/BIMS_api.conf /etc/nginx/sites-enabled/BIMS_api.conf
systemctl restart nginx.service

echo "DONE! :)"
