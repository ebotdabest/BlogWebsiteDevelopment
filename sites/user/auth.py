import flask as f
import dbmanager as dbm
import re


def sanitize_string(input_string):
    # Match against SQL meta-characters
    sql_meta_chars = re.compile(r'(%|;|,|\\|--|\*|\/|\+|-|\(|\)|=|>|<|\||`|"|\')')

    # Replace SQL meta-characters
    sanitized_string = re.sub(sql_meta_chars, "", input_string)

    return sanitized_string
auth_pages = f.Blueprint("auth_pages", __name__)

def render_issue(issue):
    return f.render_template("auth/register.html", issue=f"<div id='issue'>{issue}</div>")

@auth_pages.route("/register", methods= ["GET", "POST"])
def register():
    if len(f.request.form) != 0:

        name = sanitize_string(f.request.form.get("name").strip())
        email = sanitize_string(f.request.form.get("email").strip())
        pword = sanitize_string(f.request.form.get("pword").strip())
        pword2 = sanitize_string(f.request.form.get("pwordt").strip())
        if name != "":
            if email != "":
                if pword != "" or pword2 != "":
                    isname = dbm.checkname(name)
                    if isname:
                        isemail = dbm.checkemail(email)
                        if isemail:
                            if re.search("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email, re.IGNORECASE):
                                if pword == pword2:
                                    dbm.register_account(name, pword, email)
                                    return f.redirect("/login")
                                else:
                                    return render_issue("Passwords don't match")
                            else:
                                return render_issue("Email is not valid")
                        else:
                            return render_issue("Email is already in use")
                    else:
                        return render_issue("Name is already taken")
                else:
                    return render_issue("Password cannot be empty")
            else:
                return render_issue("Email cannot be empty")
        else:
            return render_issue("Name cannot be empty")

    else:
        return f.render_template("auth/register.html")

def render_login_issue(issue):
    return f.render_template("auth/login.html", issue=f"<div id='issue'>{issue}</div>")

@auth_pages.route("/login", methods=["GET", "POST"])
def login():
    if len(f.request.form) != 0:
        email = sanitize_string(f.request.form.get("email").strip())
        pword = sanitize_string(f.request.form.get("pword").strip())
        login_resp = dbm.login_account(email, pword)
        if login_resp["resp"] is True:
            f.session["user"] = {
                "name": login_resp["name"],
                "pfp": f"/pfp/{login_resp['id']}",
                "token": login_resp["token"],
                "email": login_resp["email"],
                "id":login_resp["id"]
            }
            return f.redirect("/")
        else:
            return render_login_issue("Incorrect email/password")

    else:
        return f.render_template("auth/login.html")

@auth_pages.route("/logout")
def logout():
    f.session["user"] = None
    f.session["editor_session"] = None
    return f.redirect("/")