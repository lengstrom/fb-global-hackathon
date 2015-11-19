import pdb, time, os, json
import tornado.httpserver
import tornado.ioloop
import numpy as np
import tornado.web
from tornado.options import define, options

class FingerPrinter(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def get(self):
        self.render("index.html")

    def post(self):
        # if there's a face (or was in the last two seconds): send the coordinates of the image (x, y, h, w)
        # otherwise send '_
        pdb.set_trace()
        # self.request.body
        
        res = "{}"
        
        self.write(res)

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", ImageHandler, dict())
    ])
    server = tornado.httpserver.HTTPServer(app)
    server.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
