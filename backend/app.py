from backend.blueprints import *
from flask import send_from_directory
from config import UPLOADFLOADER
from manage import app, logger

app.register_blueprint(admin_routes, url_prefix='/admin')
app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(posts, url_prefix='/posts')


@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(UPLOADFLOADER, filename)


if __name__ == "__main__":
    logger.log("info", "app.py | server is starting on port:8080")
    app.run(debug=False, port=8080, host='0.0.0.0')

