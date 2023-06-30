import flask as f
from sites.index import index
from sites.user.auth import auth_pages
from sites.posts.creator import editor_bp
from sites.posts.viewer import viewer_bp
from flask_session import Session
import dbmanager as dbm

app = f.Flask(__name__)
app.config['SECRET_KEY'] = "david"


@app.context_processor
def utility_processor():
    def render_user():
        if f.session.get("user") != None:
            if f.session["user"]["pfp"] != "":
                return '<button onclick="showYes()" id="user-holder">'\
                    f'<img src="{f.session["user"]["pfp"]}" alt="pfp">'\
                    f'<p>{f.session["user"]["name"]}</p>'\
                    '</button>'
            else:
                return '<button onclick="showYes()" id="user-holder">' \
                       '<img src="static/imgs/cat.png" alt="pfp">' \
                       f'<p>{f.session["user"]["name"]}</p>' \
                       '</button>'
        else:
            return '<a href="/login" id="user-holder" class="login-btn">Login</a>'


    return dict(render_user = render_user)

app.register_blueprint(index)
app.register_blueprint(auth_pages)
app.register_blueprint(editor_bp)
app.register_blueprint(viewer_bp)
import os

@app.route("/upload",  methods=['POST'])
def upl():
    if 'file' not in f.request.files:
        return 'No file part'
    file = f.request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = file.filename
        file_bytes = file.read()

        # print(file_bytes)
        dbm.change_picture(f.session["user"]["id"], f.session["user"]["token"], file_bytes)
        return f.redirect("/")
import io

@app.route("/pfp/<id>")
def load_pfp(id):
    pfp_bytes:bytes = dbm.loadpfp(id)
    return f.send_file(io.BytesIO(pfp_bytes), download_name="pfp.png")

# @app.route("/test")
# def test_logged():
#     f.session["user"] = {
#         "name": "Jhon Doe",
#         "pfp": "static/imgs/cat.png"
#     }
#     return f.redirect("/")

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8932)
