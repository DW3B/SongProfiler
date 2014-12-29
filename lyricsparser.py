import urllib2, re
from bs4 import BeautifulSoup

class LyricParser(object):
	def __init__(self, track=None, artist=None):
		self.track = re.sub('[\W_]+', '', track.lower())
		self.artist = re.sub('[\W_]+', '', artist.lower())
		self.url = 'http://www.azlyrics.com/lyrics/%s/%s.html' % (self.artist, self.track)
		try:
			self.lyrics = BeautifulSoup(urllib2.urlopen(self.url).read()).select('div[style="margin-left:10px;margin-right:10px;"]')[0].text.encode('utf-8')
		except:
			raise Exception('Could not locate URL for lyrics')

	def word_list(self):
		line_list = []
		for line in self.lyrics.split('\n'):
			if len(line) != 0:
				try:
					if list(line)[0] != '[':
						line = re.sub('[\(\)\?,\.\!]', '', line).lower()
						re_line = re.search('\W(\d)x\W', line)
						if re_line:
							for x in range(0, int(re_line.group(0)) - 1):
								line_list.append(line.replace(re_line.group(1), ''))
						else:
							line_list.append(line)
				except:
					continue
		return ' '.join(line_list).split(' ')

	def unique_words(self):
		unique = []
		for w in self.word_list():
			if not w in unique:
				unique.append(w)
		return sorted(unique)
		
