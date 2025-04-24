#!/bin/sh

# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░ЗАПУСКАЕМ░ГУСЕЙ-РАЗВЕДЧИКОВ░░░░
# ░░░░░▄▀▀▀▄░░░▄▀▀▀▀▄░░░▄▀▀▀▄░░░░░
# ▄███▀░◐░░░▌░▐0░░░░0▌░▐░░░◐░▀███▄
# ░░░░▌░░░░░▐░▌░▐▀▀▌░▐░▌░░░░░▐░░░░
# ░░░░▐░░░░░▐░▌░▌▒▒▐░▐░▌░░░░░▌░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

python -m flask db init
python -m flask db migrate
python -m flask db upgrade

echo $FLASK_DEBUG
if [ "$FLASK_DEBUG" == "1" ]; then
        python -m flask run --host=0.0.0.0 --port=8080
else
        gunicorn --workers=4 --worker-class=gevent your_app:app --timeout 90
fi

exec "$@"
