import urllib2, spotipy, re
from lyricsparser import LyricParser
from bs4 import BeautifulSoup

HOT100_URL = 'http://www.billboard.com/charts/hot-100'
SOUP = BeautifulSoup(urllib2.urlopen(HOT100_URL).read())
SPOT = spotipy.Spotify()

SONG_LIST = []
p = 0
for song in SOUP.findAll('article'):
	songTitle = song.select('h2')[0].text
	if '\n' in songTitle:
		p += 1
		songDict = {
			'track'		: songTitle.strip('\n\t'),
			'artist' 	: song.select('a[href^="http://www.billboard.com/artist"]')[0].text.strip('\n\t'),
			'position' 	: p
		}
		try:
			parser = LyricParser(track=songDict['title'], artist=songDict['artist'])
			words = parser.word_list()
			songDict['word_count'] = len(words)
			songDict['unique_words'] = []
			for w in words:
				if not w in songDict['unique_words']:
					songDict['unique_words'].append(w)
		except:
			continue
		spotifyTag = song.select('a[href^="https://embed.spotify.com/?uri=spotify"]')
		if len(spotifyTag) > 0:
			songDict['uri'] = unicode(re.search('(spotify:track:)\w{22}', spotifyTag[0].get('href')).group(0))
		else:
			try:
				songDict['uri'] = unicode(SPOT.search(q='%s' % songDict['track'])['tracks']['items'][0]['uri'])
			except:
				songDict['uri'] = None
		if songDict['uri'] != None:
			sData = SPOT.track(songDict['uri'])
			songDict['album'] = sData['album']['name']
			songDict['img_url'] = sData['album']['images'][0]['url']
			songDict['length'] = sData['duration_ms']
		SONG_LIST.append(songDict)

for s in SONG_LIST:
	print s
	
