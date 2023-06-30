import flask as f


index = f.Blueprint("index", __name__)

@index.route("/")
def index_site():
    return f.render_template("index.html")