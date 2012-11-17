import tornado.ioloop
import tornado.options
from tornado import options
import tornado.httpserver
import os
import tornado.web
import sqlite3
from subprocess import Popen, PIPE
import json


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/search", Search),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"), 
            debug=True,
            autoescape=None
            )
        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "index.html",
            page_title = "who knows",
        ) 

class Search(tornado.web.RequestHandler):
    def get(self):
        keyword = self.get_argument('keyword')
        keyword = str(keyword.encode('latin-1', 'replace'))

        pp = Popen('python fancyapi.py', shell=True, stdout=PIPE)
        stdout_list = []
        for ln in pp.stdout:
            try:
                stdout_list.append(ln)
            except Exception, e:
                pass

        #sqlite db setup
        con = sqlite3.connect('professors.db')
        cur = con.cursor()
        professors = []

        for s in stdout_list[0]:
           # db row fetch
            cur.execute("select email, image_url, dept from professors where id = ?", (s))
            rows = cur.fetchall()
            for row in rows:
                id = s
                email = row[0]
                image_url = row[1]
                dept = row[2]

                professor = {'id' : int(s), 'email' : email, 'image_url' : image_url, 'dept' : dept}
                professors.append(professor)

        self.write(json.dumps(professors))

def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen("9999")
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
