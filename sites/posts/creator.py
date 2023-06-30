import flask as f
from functions import MarkdownToHTML
import dbmanager as dbm

editor_bp = f.Blueprint("editor_bp", __name__)


@editor_bp.route("/api/save", methods=["GET","POST"])
def save():
    if f.request.form.get("content") != None:
        dbm.edit_post(f.session["editor_session"]["id"], f.request.form.get("content"), f.request.form.get("post-name"),
                      f.session["user"]["token"])
        return f.redirect(f"/editor/{f.session['editor_session']['id']}")
    else:
        return f.redirect("/")


@editor_bp.route("/editor/<id>")
def post_editor(id):
    f.session["editor_session"]["id"] = id
    loaded_content = dbm.load_content(id)
    try:
        if loaded_content["creator"] == f.session["user"]["token"]:
            return f.render_template("post/post.html", id=id, content=loaded_content["content"],
                                     title=loaded_content["name"])
        else:
            return f.redirect("/api/preview")
    except Exception:
        return f.render_template("post/failed_editor.html", id=id)


@editor_bp.route("/editor")
def open_editor():
    if f.session["user"] != None:
        posts = dbm.get_all_posts(f.session["user"]["token"])
        if len(posts) < 100:
            dbm.create_post(f.session["user"]["token"])
            id = dbm.last_id()
            f.session["editor_session"] = {
                "id": id
            }
            return f.redirect(f"/editor/{id}")
        else:
            return f.render_template("post/failed.html")
    else:
        return f.redirect("/login")

@editor_bp.route("/api/preview")
def preview():
    if f.request.args.get("id") != None:
        converter = MarkdownToHTML()
        data = dbm.load_content(f.request.args.get("id"))
        if data["resp"]:
            converted = converter.markdown_to_html(data["content"])
            return f.render_template("post/renderer.html", content=converted)
        else:
            return f.render_template("post/renderer.html", content="Cannot load post")
    else:
        return f.redirect("/")
