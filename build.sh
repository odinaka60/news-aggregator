set -o errexit  # exit on error

pip install -r ./newsfeed/requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate