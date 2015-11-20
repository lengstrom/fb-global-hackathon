import sys, os, json, requests, parse_srt, pdb
from unicodedata import normalize
SONG_ID=sys.argv[1]
SONG_TITLE=sys.argv[2]
SONG_ARTIST=sys.argv[3]
GOOGLE_API_KEY=sys.argv[4]

def make_srt(lang, vid_id, und_is_en, GB_is_en):
    lang_ = lang
    if lang == 'en' and und_is_en:
        lang_ = 'und'

    if lang == 'en' and GB_is_en:
        lang_ = 'en-GB'


    xml = requests.get('http://video.google.com/timedtext?lang=' + lang_ + '&v=' + vid_id).text
    try:
        xml = normalize('NFKD', xml).encode("ASCII", 'ignore')
    except:
        print "err parsing! proceeding..."
    srt_txt = parse_srt.parseBuf(xml)
    with open('./' + lang + '.srt', 'w') as f:
        f.write(srt_txt)

URL="https://www.googleapis.com/youtube/v3/captions/?part=snippet&videoId=%s&key=%s" % (SONG_ID, GOOGLE_API_KEY)
r=requests.get(URL)
request_json = json.loads(r.text)
items=request_json['items']
items=filter(lambda x: x['kind'] == 'youtube#caption',items)
json_to_write = {
    'title':SONG_TITLE,
    'artist':SONG_ARTIST,
    'languages':[] #lang
}

for i in items:
    snip = i['snippet']
    json_to_write['languages'].append(str(snip['language']))

und_is_en = False
GB_is_en = False

json_to_write['languages'] = filter(lambda x: x in ['en', 'und', 'it', 'es', 'fr', "en-GB", 'es-MX', 'en-US', 'pt-BR'], json_to_write['languages'])

if 'und' in json_to_write['languages'] and 'en' in json_to_write['languages']:
    del json_to_write['languages'][json_to_write['languages'].index('und')]
elif 'und' in json_to_write['languages'] and not 'en' in json_to_write['languages']:
    json_to_write['languages'].append('en')
    del json_to_write['languages'][json_to_write['languages'].index('und')]
    und_is_en = True

if 'en-GB' in json_to_write['languages'] and 'en' in json_to_write['languages']:
    del json_to_write['languages'][json_to_write['languages'].index('en-GB')]
elif 'en-GB' in json_to_write['languages'] and not 'en' in json_to_write['languages']:
    json_to_write['languages'].append('en')
    del json_to_write['languages'][json_to_write['languages'].index('en-GB')]
    GB_is_en = True

    
for i in json_to_write['languages']:
    make_srt(i, SONG_ID, und_is_en, GB_is_en)

with open('song.json', 'w') as f:
    f.write(json.dumps(json_to_write))
