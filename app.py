from manage import *
from blueprints import *

app.register_blueprint(main_routes, url_prefix='/routes')
app.register_blueprint(admin_routes, url_prefix='/admin')


@app.route('/')
def index():
    return render_template('base.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return redirect("/admin/login")



if __name__ == "__main__":
    app.run(debug=True)

