from blueprints import *
from flask import send_from_directory
from config import UPLOADFLOADER, SERVER_PORT
from manage import app, logger

app.register_blueprint(admin_routes, url_prefix='/admin')
app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(posts, url_prefix='/posts')


@app.route('/ping')
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
    return send_from_directory(UPLOADFLOADER, filename)
print("for cicd")
if __name__ == "__main__":
    logger.log("info", "app.py | server is starting on port:8080")
    app.run(debug=True, port=SERVER_PORT, host='0.0.0.0')

