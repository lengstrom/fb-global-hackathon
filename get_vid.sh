# should get:
# Song title, artist name
# Youtube ID
# wav file
# english srt file
cd songs
rm -rf $1
mkdir $1
cd $1
python ../../get_song_info.py "$1" "$2" "$3" "$GOOGLE_API_KEY" #song.json
youtube-dl --extract-audio --audio-format wav "https://www.youtube.com/watch?v=${1}" -o song.wav #song.wav
ls 
cd ../..
