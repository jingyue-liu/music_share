import xml.etree.ElementTree as ET
fname = 'Playlist_new.xml'

# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>
def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None

stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict')
print 'Dict count:', len(all)
for entry in all:
	if ( lookup(entry, 'Track ID') is None ) : continue
	#lyrics = lookup(entry, 'Location')
	name = lookup(entry, 'Name')
	artist = lookup(entry, 'Artist')
	album = lookup(entry, 'Album')
	length = lookup(entry, 'Total Time') #ms
	style = lookup(entry, 'Genre')
	releaseYear = lookup(entry, 'Year')
	songWriter = lookup(entry, 'Composer')
	

	if name is None or artist is None or album is None : 
		continue
	
	print name, artist, album, length, style,releaseYear,songWriter