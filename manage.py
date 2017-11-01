import model
import hashlib
import sys
import json
import getpass

def add_user(username, password):
    passHash = hashlib.sha512(password.encode('utf-8')).hexdigest()
    model.new_user(username, passHash)
    return 0

def authenticate():
    name = input("Login:")
    password = getpass.getpass("Password:")
    model.authenticate(name, hashlib.sha512(password.encode('utf-8')).hexdigest())
    return 1


if len(sys.argv) != 1:
    if sys.argv[1] == 'addUser':
        if len(sys.argv) == 4:
            add_user(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'addPost':
        if len(sys.argv) == 3:
            filename = sys.argv[2]
            if authenticate():
                with open(filename, "r") as postFile:
                    n = json.load(postFile)
                    newPost = n['blogpost']
                    model.new_post(newPost['title'], newPost['text'], newPost['author'])
