from mysql.connector import connect
from encrypt import encrypt
import datetime as dt
import re

db = connect(
    host="localhost",
    user="root",
    password="EbotdabesT",
    database="blogdatabase"
)
cursor = db.cursor()

def sanitize_string(input_string):
    # Match against SQL meta-characters
    sql_meta_chars = re.compile(r'(%|;|,|\\|--|\*|\/|\+|-|\(|\)|=|>|<|\||`|"|\')')

    # Replace SQL meta-characters
    sanitized_string = re.sub(sql_meta_chars, "", input_string)

    return sanitized_string

from string import ascii_uppercase, ascii_lowercase
import random as r

def generate():
    numbers = "0123456789"
    letters = ascii_lowercase + ascii_uppercase + numbers
    pw = []
    for x in range(60):
        pw.append(letters[r.randint(0, len(letters) - 1)])

    return "".join(pw)


def register_account(name, password, email):
    password_encrypted = encrypt(password)
    token_generated = generate()
    sql = "INSERT INTO users (token, name, password, picture, email) VALUES (%s, %s, %s, %s, %s)"
    args = (token_generated, name, password_encrypted, "", email)

    cursor.execute(sql, args)
    db.commit()

def login_account(email, password):
    password_encrypted = encrypt(password)
    sql = "SELECT * FROM users WHERE email=%s AND password=%s"
    args = (email, password_encrypted)
    cursor.execute(sql, args)
    fecthed = cursor.fetchall()
    if len(fecthed) == 1:
        data = fecthed[0]
        return {
            "resp": True,
            "token": data[1],
            "name": data[2],
            "pfp": data[4],
            "email": data[5],
            "id":data[0]
        }
    else:
        return {"resp":False}

def create_post(creatortoken):
    sql = "INSERT INTO posts (content, creatorid, upvotes, created, name) VALUES (%s, %s, %s, %s, %s)"
    args = ("""# Example blog
## Here is where your adventure begins
[table:none]
normal,table,example
it,has,multiple
[/table]

[table:outline]
boxed,table
also,lines
[/table]

[table:outline-whole]
big,boxed,table
whoel,also,lines
[/table]

[table:outline-whole, outline]
big,boxed,table
the,whole,outlined
[/table]

This text is **Bold**
This text is *Italic*
This text is __underlined__
This is a [link](https://google.com)
This is an (image)[https://as1.ftcdn.net/v2/jpg/00/92/53/56/1000_F_92535664_IvFsQeHjBzfE6sD4VHdO8u5OHUSc6yHF.jpg]


    """.strip(), creatortoken, "0", dt.datetime.now().strftime("%m/%d/%Y %H:%M"), "Example Blog")
    cursor.execute(sql, args)
    db.commit()
    return cursor.fetchall()

def load_user(token):
    token = sanitize_string(token)
    sql = "SELECT * FROM users WHERE token = %s"
    args = (token,)
    cursor.execute(sql, args)

    return cursor.fetchone()

def load_content(id):
    sql = "SELECT * FROM posts WHERE id=%s"
    id = sanitize_string(id)
    args = (id,)
    cursor.execute(sql, args)
    fetched = cursor.fetchall()
    if len(fetched) == 1:
        return {
            "resp":True,
            "id":fetched[0][0],
            "content": fetched[0][1],
            "creator": fetched[0][2],
            "upvotes": fetched[0][3],
            "name":fetched[0][5]
        }
    else:
        return {"resp":False}

def edit_post(id, content,name, creatortoken):
    sql = "UPDATE posts SET content = %s, created = %s, name=%s WHERE id=%s AND creatorid = %s"
    args = (sanitize_string(content), dt.datetime.now().strftime("%m/%d/%Y %H:%M"), sanitize_string(name),
            sanitize_string(id), sanitize_string(creatortoken),)
    cursor.execute(sql, args)
    db.commit()

def edit_post_name(id, content, creatortoken):
    sql = "UPDATE posts SET name = %s, created = %s WHERE id=%s AND creatorid = %s"
    args = (sanitize_string(content), dt.datetime.now().strftime("%m/%d/%Y %H:%M"),
            sanitize_string(id), sanitize_string(creatortoken),)
    cursor.execute(sql, args)
    db.commit()

def delete_post():
    pass

def delete_account():
    pass

def change_password():
    pass

def change_picture(id, token, picture):
    sql = "UPDATE users SET picture = %s WHERE id=%s AND token = %s"
    args = (picture, id, token, )
    cursor.execute(sql, args)
    db.commit()
#gugu gaga = guga : https://youtube.com/@guga_food

def checkname(name):
    sql = "SELECT * FROM users WHERE name = %s"
    args = (sanitize_string(name),)

    cursor.execute(sql, args)

    fetched = cursor.fetchall()
    print(fetched)
    if len(fetched) >= 1:
        return False

    return True

def checkemail(email):
    sql2 = "SELECT * FROM users WHERE email = %s"
    args2 = (sanitize_string(email),)

    cursor.execute(sql2, args2)
    fetched = cursor.fetchall()
    print(fetched)
    if len(fetched) >= 1:
        return False

    return True

def last_id():
    sql = "SELECT * FROM posts"
    cursor.execute(sql)
    fetched = cursor.fetchall()
    return fetched[len(fetched) - 1][0]

def get_all_posts(creatortoken):
    sql = "SELECT * FROM posts WHERE creatorid = %s"
    args = (sanitize_string(creatortoken), )
    cursor.execute(sql, args)
    fetched = cursor.fetchall()
    return fetched

def loadpfp(id):
    sql = "SELECT * FROM users WHERE id = %s"
    args = (id,)
    cursor.execute(sql, args)
    fetched = cursor.fetchone()
    img = fetched[4]
    return img

# create_post("a", "")