from blueprints import *
from flask import send_from_directory
from config import UPLOADFLOADER

app.register_blueprint(admin_routes, url_prefix='/admin')
app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(posts, url_prefix='/posts')


@app.route('/')
@safe
def index():
    return redirect("/posts/news")

@app.route('/logs')
@safe
def logs():
    return render_template('logs.html', logs=session['_flashes'])


@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(UPLOADFLOADER, filename)


if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')

