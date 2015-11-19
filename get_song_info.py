import sys, os, json, requests
SONG_ID=sys.argv[1]
SONG_TITLE=sys.argv[2]
SONG_ARTIST=sys.argv[3]
GOOGLE_API_KEY=sys.argv[4]

def make_srt(lang, vid_id):
    xml = requests.get('http://video.google.com/timedtext?lang=' + lang + '&v=' + vid_id).text
    
    

URL="https://www.googleapis.com/youtube/v3/captions/?part=snippet&videoId=%s&key=%s" % (SONG_ID, GOOGLE_API_KEY)
r=requests.get(URL)
request_json = json.loads(r.text)
items=request_json['items']
items=filter(lambda x: x['kind'] == 'youtube#caption',items)
json_to_write = {
    'title':SONG_TITLE,
    'artist':SONG_ARTIST,
    'captions':[] #lang
}

for i in items:
    snip = i['snippet']
    json_to_write['captions'].append(json_to_write['language'])

with open('song.json', 'w') as f:
    f.write(json.dumps(json_to_write))

for i in json_to_write['captions']:
    make_srt(i, SONG_ID)
