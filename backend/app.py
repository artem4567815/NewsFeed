from blueprints import *
from flask import send_from_directory
from config import SERVER_PORT, UPLOAD_FOLDER, DEBUG
from manage import app, logger

app.register_blueprint(admin_routes, url_prefix='/admin')
app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(posts, url_prefix='/posts')


@app.route('/ping') #Z гений
def ping():
    return "edufeed work!", 200


@app.route("/test/drop-db", methods=["POST"])
def drop_db():
    if not app.debug:
        abort(404)
    for table in reversed(db.metadata.sorted_tables):
        db.session.query(table).delete()
    db.session.commit()
    return jsonify({"message": "Destroyed"})


@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    logger.log(f"info", "app.py | server is starting on port:{}".format(SERVER_PORT))
    app.run(debug=True, port=SERVER_PORT, host='0.0.0.0')

