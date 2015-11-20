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

def get_lines_to_display(text, offset_time):
    jso = json.loads(text)
    last = 0
    for i, v in enumerate(jso):
        curr = int(v['ts'])
        if last < offset_time and curr >= offset_time:
            selected = i
            break
        else:
            last = curr
    if selected == 0:
        lines = jso[:3]
    elif selected == len(jso) - 1:
        lines = jso[-3:]
    else:
        lines = jso[selected -1 : selected + 2]

    return lines

def get_song_info(song, lang):
    yt_id = song['song_name']
    with open(os.path.join('./songs', yt_id, 'song.json')) as data_file:    
        data = json.load(data_file)
    name = data['title']
    artist = data['artist']
    
    subtitles = filter(lambda x: 'json' in x and lang in x, os.listdir(os.path.join('./songs', yt_id)))
    if len(subtitles) == 1:
        with open(os.path.join('./songs/', yt_id, subtitles[0]), 'r') as f:
            subtitles_txt = f.read()
    else:
        return None
    jso_to_sho = json.dumps(get_lines_to_display(subtitles_txt, song['offset_seconds']))
    return {'name':name, 'artist':artist, 'subtitles':jso_to_sho}

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
    print "    identified clip as %s seconds into %s, by %s" % (info['start_time'], info['name'], info['artist'])
    send_to_firebase(info['subtitles'],info['name'],info['artist'],info['start_time'])
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
        song = djv.recognize(FileRecognizer, recording_path)
        time_stamp, lang = file_name.split(',')
        print "    ts, lang: %s, %s" % (time_stamp, lang)
        if song['confidence'] > 10:
            print "    offset: " + str(song['offset_seconds'])
            song_info = get_song_info(song, lang)
            if song_info == None:
                print "    no song bc no lyrics for song for this lang"
                no_song(self)
            else:
                sec_into_song = (song['offset_seconds'] + 10)
                song_info['start_time'] = -sec_into_song * 1000 + int(time_stamp)
                identified_song(song_info, self)
        else:
            print "    no song bc low confidence, resetting... data was: %s" % (song,)
            no_song(self)
        
        #os.remove(recording_path)

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", FingerPrinter, dict())
    ])
    server = tornado.httpserver.HTTPServer(app)
    server.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
