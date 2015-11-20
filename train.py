import sys, os, shutil
sys.path.insert(1, '../dejavu/')
from dejavu import Dejavu

def copy_all_wavs_to_dir(olddir='./songs', newdir='./fp_wavs'):
    for yt_id in filter(lambda x: x[0] != '.', os.listdir(olddir)):
        fp = os.path.join(olddir, yt_id, 'song.wav')
        new_fp = os.path.join(newdir, yt_id + ".wav")
        print fp, new_fp
        shutil.copy(fp, new_fp)
    
if 'copy' in sys.argv:
    copy_all_wavs_to_dir()

if 'train' in sys.argv:
    config = {
        "database": {
            "host": "127.0.0.1",
            "user": "root",
            "passwd":"loganlogan", 
            "db":'dejavu'
        }
    }

    djv = Dejavu(config)
    djv.fingerprint_directory("./fp_wavs", [".wav"], 5)
