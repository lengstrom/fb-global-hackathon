import pdb, time, os, json, sys, shutil, random, time
import tornado.httpserver
import tornado.ioloop
import numpy as np
import tornado.web
from tornado.options import define, options
sys.path.insert(1, '../dejavu/')
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer

from firebase import Firebase
f = Firebase('https://fbglobalhacks.firebaseio.com/')

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

def get_song_info(song, lang):
    yt_id = song['song_name']
    with open(os.path.join('./songs', yt_id, 'song.json')) as data_file:    
        data = json.load(data_file)
    name = data['title']
    artist = data['artist']
    
    subtitles = filter(lambda x: 'json' in x and lang in x, os.path.listdir(os.path.join('./songs', yt_id)))
    if len(subtitles) == 1:
        with open(os.path.join('./songs/', yt_id, subtitles[0]), 'r') as f:
            subtitles_txt = f.read()
    else:
        return None

    return {'name':name, 'artist':artist, 'subtitles':subtitles_txt}

djv = make_djv()

def send_to_firebase(lyrics, song, artist, timestamp):
    f.child("lyrics").put(lyrics)
    f.child('song').put(song)
    f.child('artist').put(artist)
    f.child("timestamp").put(timestamp)

def no_song(res):
    send_to_firebase("","","",0)
    res.write('0')

def identified_song(info, res):
    print "    identified clip as %s seconds into %s, by %s" % (info['offset_seconds'], info['name'], info['artist'])
    send_to_firebase(info['subtitles'],info['name'],info['artist'],info['offset_seconds'])
    res.write('1')
    
class FingerPrinter(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def get(self):
        self.render("index.html")

    def post(self):
        print "Post request begun..."
        global djv
        file_name = str(self.request.files.keys()[0])
        recording = self.request.files[file_name][0]['body']
        recording_path = './tmp/' + str(random.randint(1, 9999)) + '.wav'
        with open(recording_path, 'wb') as f:
            f.write(recording)
        time_stamp, lang = file_name.split(',')
        print "    ts, lang: %s, %s" % (time_stamp, lang)
        song = djv.recognize(FileRecognizer, recording_path)
        if song['confidence'] > 10:
            song_info = get_song_info(song)
            if song_info == None:
                print "    no song bc no lyrics for song for this lang"
                no_song(self)
            else:
                sec_into_song = (song['offset_seconds'] + 8)
                song_info['start_time'] = (time.time() - sec_into_song) * 1000
                identified_song(song_info, self)
        else:
            print "    no song bc low confidence, resetting..."
            no_song(self)
        
        os.remove(recording_path)

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", FingerPrinter, dict())
    ])
    server = tornado.httpserver.HTTPServer(app)
    server.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
