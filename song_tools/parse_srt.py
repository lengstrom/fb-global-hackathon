#!/usr/bin/python
import re, sys

pat = re.compile(r'<?text start="(\d+\.\d+)" dur="(\d+\.\d+)">(.*)</text>?', re.DOTALL)

def parseLine(text):
	"""Parse a subtitle."""
	m = re.match(pat, text)
	if m:
		return (m.group(1), m.group(2), m.group(3))
	else:
		return None

def formatSrtTime(secTime):
	"""Convert a time in seconds (google's transcript) to srt time format."""
	sec, micro = str(secTime).split('.')
	m, s = divmod(int(sec), 60)
	h, m = divmod(m, 60)
	return "{:02}:{:02}:{:02},{}".format(h,m,s,micro)

def convertHtml(text):
	"""A few HTML encodings replacements.
	&amp;#39; to '
	&amp;quot; to "
	"""
	return text.replace('&amp;#39;', "'").replace('&amp;quot;', '"')

def printSrtLine(i, elms):
	"""Print a subtitle in srt format."""
	return "{}\n{} --> {}\n{}\n\n".format(i, formatSrtTime(elms[0]), formatSrtTime(float(elms[0])+float(elms[1])), convertHtml(elms[2]))

def parseBuf(s): # s is all the lines as a text file
	buf = s.split('><')
	i = 0
	out_buf = []
	for text in buf:
		parsed = parseLine(text)
		if parsed:
			i += 1
			out_buf.append(printSrtLine(i, parsed) + '\n')
			
	return "".join(out_buf)

if __name__ == "__main__":
	file_name = sys.argv[1]
	print parseBuf(open(file_name, 'r').read())

import requests
lang='it'
vid_id='jofNR_WkoCE'
xml = requests.get('http://video.google.com/timedtext?lang=' + lang + '&v=' + vid_id).text
	
