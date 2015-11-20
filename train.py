import sys, os, shutil
sys.path.insert(1, '../dejavu/')
import dejavu

def copy_all_wavs_to_dir(olddir='./songs', newdir='./fp_wavs'):
    for yt_id in filter(lambda x: x[0] != '.', os.listdir(olddir)):
        fp = os.path.join(olddir, yt_id, 'song.wav')
        shutil.copy(fp, os.path.join(newdir, yt_id + '.wav'))
    
if 'copy' in sys.argv:
    copy_all_wavs_to_dir()


