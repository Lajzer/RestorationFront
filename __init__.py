import web
import sqlalchemy
from url import *
import model
import hashlib


render = web.template.render('templates', base='base')
renderBaseless = web.template.render('templates')

class Post:
    def __init__(self, t, a, d ,b):
        self.title = t
        self.author = a
        self.date = d
        self.body = b
        return

class index:
    def GET(self):
        return "hello world"

class blog:
    def GET(self):
        posts = model.get_posts()#Post("aaa","bbb","ccc","ddd")
        return render.blog(posts)

class szalupa:
    def GET(self):
        return "Szalupa page"

class login:
    form = web.form.Form(
            web.form.Textbox('login', web.form.notnull, size=30, description="Login:"),
            web.form.Password('pass', web.form.notnull, size=30, description="Password"),
            web.form.Button('Log in'))

    def GET(self):
        form = self.form()
        return render.admin(form)

    def POST(self):
        form = self.form()

        if not form.validates():
            return render.login(form)

        print(form['login'].value)
        print(form['pass'].value)
        name = form['login'].value
        passHash = hashlib.sha512(form['pass'].value.encode('utf-8'))

       # print(passHash)
       # print(name)
       # print(passHash.hexdigest())
       # print(len(passHash.hexdigest()))
        del form
        model.log_in(name, passHash.hexdigest())
        raise web.seeother('/')

class post:
    pass

class test:
    def GET(self):
        return render.test()

def notfound():
    return web.notfound(renderBaseless.notfound())

app = web.application(urls, globals())
app.notfound = notfound
if __name__ == "__main__":
    app.run()
