import web
import sqlalchemy
from url import *
import model
import hashlib


app = web.application(urls, globals())
web.config.debug = False

session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0, 'logged_in': False})
web.config._session = session

render = web.template.render('templates', globals={'context': session} ,base='base')
render_plain = web.template.render('templates', globals={'context': session})

class Post:
    def __init__(self, t, a, d ,b):
        self.title = t
        self.author = a
        self.date = d
        self.body = b
        return

class index:
    def GET(self):
        #if session.logged_in:
        session['count'] += 1
        #else:
        #    session.click -= 1
        return("hello world, counter:" + str(session['count']) + str(session['logged_in']))

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
        return render.login(form)

    def POST(self):
        form = self.form()

        if not form.validates():
            return render.login(form)

        print(form['login'].value)
        print(form['pass'].value)
        name = form['login'].value
        passHash = hashlib.sha512(form['pass'].value.encode('utf-8'))


        if not model.authenticate(name, passHash.hexdigest()):
            session['logged_in'] = True
            raise web.seeother('/admin')

        del form
        raise web.seeother('/login')

class logout:
    def GET(self):
        session['logged_in'] = False
        raise web.seeother('/')

class admin:
    form = web.form.Form(
            web.form.Textbox('Title', web.form.notnull, size=30, description="Title:"),
            web.form.Textbox('Author', web.form.notnull, size=30, description="Author:"),
            web.form.Textarea('Text', web.form.notnull, size=70, description="Text:"),
            web.form.Button('Add post'))

    def GET(self):
        form = self.form()
        if session['logged_in']:
            return render_plain.admin(form)
        else:
            raise web.notfound()
    def POST(self):
        form = self.form()

        return render_plain.admin(form)


class blogpost:
    def GET(self, postname):
        blogpost_ = postname
        return render.blogpost(blogpost_)

class test:
    def GET(self):
        return render.test()

def notfound():
    return web.notfound(render_plain.notfound())

app.notfound = notfound
if __name__ == "__main__":
    app.run()
