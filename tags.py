#!/usr/bin/env python
import os
import sys
import sqlite3
import unicodedata
import re
import time
#import mutagen
from mutagen.mp3 import MP3

# change this path as needed
#dsn = '/home/archerja/Music/id3.db3'
dsn = os.path.join(os.getcwd(),'id3.db3')
basedir = '/media/archerja/Stuff/backup/Music'
version = '0.7'

class ID3:
    def __init__(self,path):
        self._load(path)

    def _load(self, filename):
        tags = MP3(filename)
        comments = []
        for key in tags:
            if key[0:4] == 'COMM':
                if(tags[key].desc == ''):
                    comments.append(tags[key].text[0])
        comments.append('');
        self.album = tags.get('TALB', [''])[0]
        self.artist = tags.get('TPE1', [''])[0]
        self.duration = "%u:%.2d" % (tags.info.length / 60, tags.info.length % 60)
        self.length = tags.info.length
	self.bitrate = tags.info.bitrate / 1000
	self.year = str(tags.get('TDRC', [''])[0])
        self.title = tags.get('TIT2', [''])[0]
        self.comment = comments[0]
        self.genre = tags.get('TCON', [''])[0]
        self.track = tags.get('TRCK', [''])[0]

def MYinfo():
	print '--------------------'
	print 'database path: ', dsn
	print '   music path: ', basedir
	print '--------------------'


class Script:
    def build(self,start):
	startbuild = time.time()
        errors = []
	print 'database path: ', dsn
        cnx = self.db()
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM id3;")
        for root, dir, files in os.walk(start):
            for name in files:
                if name[-4:].lower() == '.mp3':
                    path = os.path.join(root,name)
		    location = path.split(basedir)[1]
#                    print name
                    print ".",
                    try:
                        id3 = ID3(path)
                    except:
                        errors.append(path)
                        id3 = None
                    if id3 != None:
                        cursor.execute("INSERT INTO id3(artist, album, track, title, genre, bitrate, year, comment, duration, location) VALUES(?,?,?,?,?,?,?,?,?,?)",
                                       (id3.artist,id3.album,id3.track,id3.title,id3.genre,id3.bitrate,id3.year,id3.comment,id3.duration,location))
        cnx.commit()
        if len(errors) > 0:
            print ""
            print "---- Errors ----"
            print ""
            for error in errors:
                print error
	endbuild = time.time()
	print 'database built in', "%g" % round((endbuild - startbuild),2), 'seconds'
	print ''

    def test(self,query):
	MYinfo()
        cnx = self.db()
        cursor = cnx.cursor()
	print 'command line query: ', query
        locsplit = query.split(basedir)[1]
	print 'location path only: ', locsplit
	print '--------------------'
        q = 'SELECT * from id3 WHERE location LIKE ' + '"' + locsplit + '%"' + ' ORDER BY location'
        cursor.execute(q)
	print 'records in database:'
	print '--------------------'
        for line in cursor:
            print line["location"]
	print '--------------------'
        print 'files to update:'
	print '--------------------'
        for root, dir, files in os.walk(query):
            for name in files:
                if name[-4:].lower() == '.mp3':
                    path = os.path.join(root,name)
		    location = path.split(basedir)[1]
		    print location
	print ''

    def update(self,query):
	MYinfo()
        cnx = self.db()
        cursor = cnx.cursor()
        locsplit = query.split(basedir)[1]
        q = 'DELETE from id3 WHERE location LIKE ' + '"' + locsplit + '%"'
        cursor.execute(q)
        errors = []
        for root, dir, files in os.walk(query):
            for name in files:
                if name[-4:].lower() == '.mp3':
                    path = os.path.join(root,name)
		    location = path.split(basedir)[1]
                    print location
                    try:
                        id3 = ID3(path)
                    except:
                        errors.append(path)
                        id3 = None
                    if id3 != None:
                        cursor.execute("INSERT INTO id3(artist, album, track, title, genre, bitrate, year, comment, duration, location) VALUES(?,?,?,?,?,?,?,?,?,?)",
                                       (id3.artist,id3.album,id3.track,id3.title,id3.genre,id3.bitrate,id3.year,id3.comment,id3.duration,location))
        cnx.commit()
        if len(errors) > 0:
            print ""
            print "---- Errors ----"
            print ""
            for error in errors:
                print error
	print 'database updated.'
	print ''

    def searchartist(self,query):
	MYinfo()
        cnx = self.db()
        cursor = cnx.cursor()
        q = 'SELECT * from id3 WHERE artist LIKE ' + '"%' + query + '%"' + ' ORDER BY location'
        cursor.execute(q)
        for line in cursor:
            print line["bitrate"], "*", line["artist"], "*", line["year"], "*", line["album"], "*", line["title"]
	print ''

    def searchalbum(self,query):
	MYinfo()
        cnx = self.db()
        cursor = cnx.cursor()
        q = 'SELECT * from id3 WHERE album LIKE ' + '"%' + query + '%"' + ' ORDER BY location'
        cursor.execute(q)
        for line in cursor:
            print line["bitrate"], "*", line["album"], "*", line["year"], "*", line["artist"], "*", line["title"]
	print ''

    def searchtitle(self,query):
	MYinfo()
        cnx = self.db()
        cursor = cnx.cursor()
        q = 'SELECT * from id3 WHERE title LIKE ' + '"%' + query + '%"' + ' ORDER BY location'
        cursor.execute(q)
        for line in cursor:
            print line["bitrate"], "*", line["artist"], "*", line["year"], "*", line["album"], "*", line["title"]
	print ''

    def searchgenre(self,query):
	MYinfo()
        cnx = self.db()
        cursor = cnx.cursor()
        q = 'SELECT * from id3 WHERE genre LIKE ' + '"%' + query + '%"' + ' ORDER BY location'
        cursor.execute(q)
        for line in cursor:
            print line["bitrate"], "*", line["genre"], "*", line["artist"], "*", line["year"], "*", line["album"], "*", line["title"]
	print ''

    def summary(self,query):
	MYinfo()
        cnx = self.db()
        cursor = cnx.cursor()
        if "all" in query:
          q = 'select count(distinct artist||album)||'"' albums '"' as albums ,count(distinct artist)||'"' artists '"' as artists ,count(*)||'"' total records'"' as total from id3'
          cursor.execute(q)
          for line in cursor:
              print line["albums"], line["artists"], line["total"]
        elif "genre" in query:
          q = 'select genre ,count(*) as total from id3 group by genre order by genre'
          cursor.execute(q)
          print 'totals  genre'
	  print '--------------------'
          for line in cursor:
              print "{:<7}".format(line["total"]), line["genre"]
        elif "bitrate" in query:
          q = 'SELECT "000-128" as range, count(*) as total FROM id3 where bitrate between 0 and 128 union SELECT "129-192" as range, count(*) as total FROM id3 where bitrate between 129 and 192 union SELECT "193-256" as range, count(*) as total FROM id3 where bitrate between 193 and 256 union SELECT "257-320" as range, count(*) as total FROM id3 where bitrate between 257 and 320'
          cursor.execute(q)
	  print 'range   totals'
	  print '--------------------'
          for line in cursor:
              print line["range"], line["total"]
        elif "group" in query:
          q = "SELECT substr(substr(location,(instr(location,'/')) + 1),1,(instr(substr(location,(instr(location,'/')) + 1),'/'))-1) as groups, count(*) as total FROM id3 group by substr(substr(location,(instr(location,'/')) + 1),1,(instr(substr(location,(instr(location,'/')) + 1),'/'))-1) order by substr(substr(location,(instr(location,'/')) + 1),1,(instr(substr(location,(instr(location,'/')) + 1),'/'))-1)"
          cursor.execute(q)
          print 'groups       total'
	  print '--------------------'
          for line in cursor:
              print "{:<12}".format(line["groups"]), line["total"]
	print ''

    def path320(self,query):
	MYinfo()
        cnx = self.db()
        cursor = cnx.cursor()
        locsplit = query.split(basedir)[1]
        q = 'SELECT * from id3 WHERE location LIKE ' + '"' + locsplit + '%"' + ' and bitrate < 320 ORDER BY location'
        cursor.execute(q)
        for line in cursor:
            print line["bitrate"], "*", line["artist"], "*", line["year"], "*", line["album"], "*", line["title"]

    def db(self):
        if getattr(self,"database", None) == None:
            self.database = sqlite3.connect(dsn)
            self.database.row_factory = sqlite3.Row
            self.database.text_factory = str
            cursor = self.database.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS id3(id INTEGER PRIMARY KEY AUTOINCREMENT, artist, album, track, title, genre, bitrate, year, comment, duration, location UNIQUE)")
        return self.database

if __name__ == '__main__':
    if len(sys.argv) < 3:
	print ''
        print sys.argv[0], ', version ', version
	MYinfo()
        print ''
        print 'Usage: ', sys.argv[0], ' {command}   {data}'
	print '                    db-build    [your music root path]'
	print '                                (only use first time, will delete all records)'
	print ''
	print '                    test        [music path to update]'
	print '                                (make sure...)'
	print ''
	print '                    update      [music path to update]'
	print '                                (updates the database)'
	print ''
	print '                    not320      [music path to search]'
	print '                                (checks database for records below 320 bitrate)'
	print ''
	print '       Database Searches: (using "like")'
	print '                    artist      "string"'
	print '                    album       "string"'
	print '                    title       "string"'
	print '                    genre       "string"'
	print ''
	print '       Database Summaries:'
	print '                    summary     all'
	print '                    summary     genre'
	print '                    summary     bitrate'
	print '                    summary     group'
	print ''
    else:
        script = Script()
        if sys.argv[1] == 'db-build':
            script.build(sys.argv[2])
        elif sys.argv[1] == 'test':
            script.test(sys.argv[2])
        elif sys.argv[1] == 'update':
            script.update(sys.argv[2])
        elif sys.argv[1] == 'summary':
            script.summary(sys.argv[2])
        elif sys.argv[1] == 'artist':
            script.searchartist(sys.argv[2])
        elif sys.argv[1] == 'album':
            script.searchalbum(sys.argv[2])
        elif sys.argv[1] == 'title':
            script.searchtitle(sys.argv[2])
        elif sys.argv[1] == 'genre':
            script.searchgenre(sys.argv[2])
        elif sys.argv[1] == 'not320':
            script.path320(sys.argv[2])

