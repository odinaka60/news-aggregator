set -o errexit  # exit on error

pip install -r ./newsfeed/requirements.txt

python ./newsfeed/manage.py collectstatic --no-input
python ./newsfeed/manage.py migrate