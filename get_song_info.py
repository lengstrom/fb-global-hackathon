import sys, os, json, requests, xml2json, pdb
from unicodedata import normalize
if len(sys.argv) == 2:
    for i in range(3):
        sys.argv.insert('1')
SONG_ID=sys.argv[2]
SONG_TITLE=sys.argv[3]
SONG_ARTIST=sys.argv[4]
GOOGLE_API_KEY=sys.argv[1]

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

json_to_write['languages'] = filter(lambda x: x in ['en', 'und', 'vi', 'es', 'fr', "en-GB", 'es-MX', 'en-US', 'pt-BR', 'ja'], json_to_write['languages'])

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
    print '______________________'
    print i, SONG_ID
    xml2json.make_json_from_xml(i, SONG_ID, und_is_en, GB_is_en)
    print "----------------------"

#with open('song.json', 'w') as f:
#    f.write(json.dumps(json_to_write))
