import pdb, time, os, json, sys, shutil, random
import tornado.httpserver
import tornado.ioloop
import numpy as np
import tornado.web
from tornado.options import define, options
sys.path.insert(1, '../dejavu/')
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer
import 

def make_djv():
    config = {
        "database": {
            "host": "127.0.0.1",
            "user": "root",
            "passwd":"loganlogan", 
            "db":'dejavu'
        },
        'database_type':'mysql'
    }

    return Dejavu(config)

def get_lyrics_for_lang_and_id(yt_id, lang, i):
    poss = filter(lambda x: 'srt' in x, os.listdir(os.path.join('./songs', yt_id)))
    poss = filter(lambda x: lang in x, poss)
    if len(poss) == 1:
        pdb.set_trace()
    else:
        print "len: " + len(poss)
        return None
    

djv = make_djv()

class FingerPrinter(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def get(self):
        self.render("index.html")

    def post(self):
        global djv
        file_name = str(self.request.files.keys()[0])
        recording = self.request.files[file_name][0]['body']
        recording_path = './tmp/' + str(random.randint(1, 9999)) + '.wav'
        with open(recording_path, 'wb') as f:
            f.write(recording)
        song = djv.recognize(FileRecognizer, recording_path)
        
        os.remove(recording_path)
        self.write('')

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", FingerPrinter, dict())
    ])
    server = tornado.httpserver.HTTPServer(app)
    server.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
