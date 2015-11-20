import requests, json, pdb
import wave
import contextlib

def populate():
    with open('tmp/allcodes.json', 'r') as f:
        s = f.read()
        js = json.loads(s)

    for i in js:
        yt_id = i['metadata']['filename'][len('./fp_wavs/'):-len('.wav')]
        payload = {
            'fp_code':i['code'][:50],
            'track_id':yt_id,
            'codever':'4.12',
            'length':float(i['metadata']['duration'])
        }
        requests.post("http://0.0.0.0:8080/ingest", data=payload).text

def query(url):
    
