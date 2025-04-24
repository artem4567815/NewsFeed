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
        gunicorn -w 2 -b 0.0.0.0:8080 wsgi:app --timeout 90
fi

exec "$@"
