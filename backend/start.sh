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

if [ "$FLASK_DEBUG" == "1" ]; then
        python -m flask run --host=0.0.0.0 --port=8080
else
        gunicorn -w 4 -b 0.0.0.0:8080 wsgi:app
fi

exec "$@"