import flask as f
import dbmanager as dbm
from functions import MarkdownToHTML

viewer_bp = f.Blueprint("viewver_bp", __name__)

@viewer_bp.route("/view/<id>")
def view(id):
    content = dbm.load_content(id)
    if content["resp"]:
        creator = dbm.load_user(content["creator"])
        data = {
            "name": creator[2],
            "pfp": creator[4],
            "content": content["content"],
            "title": content["name"]
        }
        converter = MarkdownToHTML()
        converted = converter.markdown_to_html(data["content"])
        return f.render_template("post/view.html", content=converted, title=data["title"],
                                 pfp = data["pfp"], creatorName=data["name"])
    else:
        return f.redirect("/")
