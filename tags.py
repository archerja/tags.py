#!/usr/bin/env python3
import os
import sys
import sqlite3
import unicodedata
import re
import time
#import mutagen
from mutagen.mp3 import MP3

# change this path as needed
dsn = os.path.join(os.getcwd(),'id3.db3')
#basedir = '/media/archerja/Extreme SSD/Music'
basedir = '/home/archerja/Music/music'
version = '0.8.0'

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
        self.bitrate = int(tags.info.bitrate / 1000)
        self.year = str(tags.get('TDRC', [''])[0])
        self.title = tags.get('TIT2', [''])[0]
        self.comment = comments[0]
        self.genre = tags.get('TCON', [''])[0]
        self.track = tags.get('TRCK', [''])[0]


def MYinfo():
        print ('--------------------')
        print ('database path: ', dsn)
        print ('   music path: ', basedir)
        print ('--------------------')


def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts


class Script:
    def build(self,start):
        startbuild = time.time()
        errors = []
        print ('')
        print ('database path: ', dsn)
        print ('')
        response = input('Create/Rebuild database from scratch? (y/N) ')
        if 'y' in response:
            cnx = self.db()
            cursor = cnx.cursor()
            cursor.execute("DELETE FROM id3;")
            for root, dir, files in os.walk(start):
                for name in files:
                    if name[-4:].lower() == '.mp3':
                        path = os.path.join(root,name)
                        location = path.split(basedir)[1]
                        section = splitall(location)[1]
                        print (".", end='')
                        try:
                            id3 = ID3(path)
                        except:
                            errors.append(path)
                            id3 = None
                        if id3 != None:
                            cursor.execute("INSERT INTO id3(artist, album, track, title, genre, bitrate, year, comment, duration, section, location) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                                           (id3.artist,id3.album,id3.track,id3.title,id3.genre,id3.bitrate,id3.year,id3.comment,id3.duration,section,location))
            cnx.commit()
            if len(errors) > 0:
                print ("")
                print ("---- Errors ----")
                print ("")
                for error in errors:
                    print (error)
            endbuild = time.time()
            print ('database built in', "%g" % round((endbuild - startbuild),2), 'seconds')
            print ('')
        else:
            print ('Nothing done.')


    def update(self,query):
        MYinfo()
        cnx = self.db()
        cursor = cnx.cursor()
        locsplit = query.split(basedir)[1]
        print ('location path only: ', locsplit)
        print ('--------------------')
        q = 'SELECT * from id3 WHERE location LIKE ' + '"' + locsplit + '%"' + ' ORDER BY location'
        cursor.execute(q)
        print ('records in database:')
        print ('--------------------')
        for line in cursor:
            print (line["location"])
        print ('--------------------')
        print ('files to update:')
        print ('--------------------')
        for root, dir, files in os.walk(query):
            for name in sorted(files):
                if name[-4:].lower() == '.mp3':
                    path = os.path.join(root,name)
                    location = path.split(basedir)[1]
                    section = splitall(location)[1]
                    print (location)
        print ('')
        response = input('Update the database for the current music folder? (y/N) ')
        if 'y' in response:
            q = 'DELETE from id3 WHERE location LIKE ' + '"' + locsplit + '%"'
            cursor.execute(q)
            errors = []
            for root, dir, files in os.walk(query):
                for name in files:
                    if name[-4:].lower() == '.mp3':
                        path = os.path.join(root,name)
                        location = path.split(basedir)[1]
                        section = splitall(location)[1]
                        print (location)
                        try:
                            id3 = ID3(path)
                        except:
                            errors.append(path)
                            id3 = None
                        if id3 != None:
                            cursor.execute("INSERT INTO id3(artist, album, track, title, genre, bitrate, year, comment, duration, section, location) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                                           (id3.artist,id3.album,id3.track,id3.title,id3.genre,id3.bitrate,id3.year,id3.comment,id3.duration,section,location))
            cnx.commit()
            if len(errors) > 0:
                print ("")
                print ("---- Errors ----")
                print ("")
                for error in errors:
                    print (error)
            print ('database updated.')
        else:
            print ('database was NOT updated.')


    def m3u(self,q1,q2,q3,q4):
        cnx = self.db()
        cursor = cnx.cursor()
        q = 'SELECT * from id3 WHERE artist LIKE '  + '"%' + q1 + '%"' + ' and album LIKE ' + '"%' + q2 + '%"' + ' and title LIKE ' + '"%' + q3 + '%"' + ' and year LIKE ' + '"%' + q4 + '%"' + ' ORDER BY location'
        cursor.execute(q)
        for line in cursor:
            print (basedir+line["location"])
        print ('')


    def search(self,query1,query2):
        MYinfo()
        cnx = self.db()
        cursor = cnx.cursor()
        if "artist" in query1:
          q = 'SELECT * from id3 WHERE artist LIKE ' + '"%' + query2 + '%"' + ' ORDER BY location'
          cursor.execute(q)
          print ('bitrate, artist, year, comment, album, track, title')
          print ('-----------------------------------------------------')
          for line in cursor:
              print (line["bitrate"], "*", line["artist"], "*", line["year"], "*", line["comment"], "*", line["album"], "*", line["track"], "*", line["title"])
          print ('')
        elif "album" in query1:
          q = 'SELECT * from id3 WHERE album LIKE ' + '"%' + query2 + '%"' + ' ORDER BY location'
          cursor.execute(q)
          print ('bitrate, album, year, comment, track, artist, title')
          print ('-----------------------------------------------------')
          for line in cursor:
              print (line["bitrate"], "*", line["album"], "*", line["year"], "*", line["comment"], "*", line["track"], "*", line["artist"], "*", line["title"])
          print ('')
        elif "title" in query1:
          q = 'SELECT * from id3 WHERE title LIKE ' + '"%' + query2 + '%"' + ' ORDER BY artist, album'
          cursor.execute(q)
          print ('bitrate, artist, album, comment, track, title')
          print ('-----------------------------------------------')
          for line in cursor:
              print (line["bitrate"], "*", line["artist"], "*", line["album"], "*", line["comment"], "*", line["track"], "*", line["title"])
          print ('')
        elif "genre" in query1:
          q = 'SELECT * from id3 WHERE genre LIKE ' + '"%' + query2 + '%"' + ' ORDER BY location'
          cursor.execute(q)
          print ('bitrate, genre, artist, year, album, track, title')
          print ('---------------------------------------------------')
          for line in cursor:
              print (line["bitrate"], "*", line["genre"], "*", line["artist"], "*", line["year"], "*", line["album"], "*", line["track"], "*", line["title"])
          print ('')
        elif "discog" in query1:
          q = 'SELECT distinct section as groups, artist||" * "||album as artalb, artist, album, year, bitrate from id3 WHERE artist LIKE ' + '"%' + query2 + '%"' + ' GROUP BY artist||" * "||album ORDER BY location'
          cursor.execute(q)
          print ('group, bitrate, year, artist, album')
          print ('-------------------------------------')
          for line in cursor:
              print (line["groups"], "*", line["bitrate"], "*", line["year"], "*", line["artist"], "*", line["album"])
          print ('')
        elif "list" in query1:
          q = 'SELECT distinct section as groups, rtrim(location, replace(location, "/", "")) as paths,artist, album, year, bitrate, location from id3 WHERE section LIKE ' + '"%' + query2 + '%"' + ' GROUP BY paths ORDER BY location'
          cursor.execute(q)
          print ('bitrate, directory path')
          print ('-------------------------------------')
          for line in cursor:
              print (line["bitrate"], "*", line["paths"])
          print ('')
        elif "bitrate" in query1:
          q = "SELECT section as groups,* from id3 WHERE bitrate = " + query2 + " ORDER BY location"
          cursor.execute(q)
          print ('bitrate, group, album, year, artist, title')
          print ('--------------------------------------------')
          for line in cursor:
              print (line["bitrate"], "*", line["groups"], "*", line["album"], "*", line["year"], "*", line["artist"], "*", line["title"])
          print ('')
        elif "below320" in query1:
          q = 'SELECT distinct section as groups, artist||" * "||album as artalb, year, bitrate from id3 WHERE substr(substr(location,(instr(location,"/")) + 1),1,(instr(substr(location,(instr(location,"/")) + 1),"/"))-1) LIKE ' + '"' + query2 + '%"' + ' and bitrate < 320 GROUP BY artist||" * "||album, bitrate ORDER BY location'
          cursor.execute(q)
          print ('group, bitrate, artist, album')
          print ('-------------------------------')
          for line in cursor:
              print (line["groups"], "*", line["bitrate"], "*", line["artalb"])
          print ('')
        else:
          print (' Incorrect command.')


    def summary(self,query):
        MYinfo()
        cnx = self.db()
        cursor = cnx.cursor()
        if "genre" in query:
          q = 'select genre ,count(*) as total from id3 group by genre order by genre'
          cursor.execute(q)
          print ('totals, genre')
          print ('---------------')
          for line in cursor:
              print ("{:<7}".format(line["total"]), line["genre"])
        elif "bitrate" in query:
          q = 'SELECT "000-128" as range, count(*) as total FROM id3 where bitrate between 0 and 128 union SELECT "129-192" as range, count(*) as total FROM id3 where bitrate between 129 and 192 union SELECT "193-256" as range, count(*) as total FROM id3 where bitrate between 193 and 256 union SELECT "257-319" as range, count(*) as total FROM id3 where bitrate between 257 and 319 union SELECT "320-999" as range, count(*) as total FROM id3 where bitrate between 320 and 999'
          cursor.execute(q)
          print ('range, totals')
          print ('---------------')
          for line in cursor:
              print (line["range"], line["total"])
        elif "year" in query:
          q = "SELECT distinct year as year, count(*) as total FROM id3 group by year order by year"
          cursor.execute(q)
          print ('year, totals')
          print ('----------------')
          for line in cursor:
              print ("{:<12}".format(line["year"]), line["total"])
        elif "group" in query:
          q = "SELECT section as groups, count(*) as total FROM id3 group by section order by section"
          cursor.execute(q)
          print ('groups, totals')
          print ('----------------')
          for line in cursor:
              print ("{:<12}".format(line["groups"]), line["total"])
        elif "artist" in query:
          q = 'select artist, count(distinct artist||album) as total from id3 where upper(substr(location,1,8)) = upper("/Artist/") group by artist order by artist'
          cursor.execute(q)
          print ('albums, artist')
          print ('----------------')
          for line in cursor:
              print ("{:<4}".format(line["total"]), line["artist"])
        else:
          q = 'select count(distinct artist||album)||'"' albums '"' as albums ,count(distinct artist)||'"' artists '"' as artists ,count(*)||'"' total records'"' as total from id3'
          cursor.execute(q)
          for line in cursor:
              print (line["albums"], line["artists"], line["total"])
        print ('')


    def db(self):
        if getattr(self,"database", None) == None:
            self.database = sqlite3.connect(dsn)
            self.database.row_factory = sqlite3.Row
            self.database.text_factory = str
            cursor = self.database.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS id3(id INTEGER PRIMARY KEY AUTOINCREMENT, artist, album, track, title, genre, bitrate, year, comment, duration, section, location UNIQUE)")
        return self.database


def help():
        print ('')
        print (sys.argv[0], ', version ', version)
        MYinfo()
        print ('')
        print ('Usage: ', sys.argv[0], ' [ summary | search | update | m3u | db-build ] {argument} {query}')
        print ('')
        print ('                    db-build    [your music root path]')
        print ('                                (only use first time, will delete all records)')
        print ('')
        print ('                    update      [music path to update]')
        print ('                                (updates the database)')
        print ('')
        print ('       Database Searches:')
        print ('                    search      artist      "string" (using "like")')
        print ('                    search      album       "string" (using "like")')
        print ('                    search      title       "string" (using "like")')
        print ('                    search      genre       "string" (using "like")')
        print ('                    search      discog      "string" (using "like", for artist)')
        print ('                    search      list        "group"  (using "like")')
        print ('                    search      below320    "group"  (using "like")')
        print ('                    search      bitrate     "string" (128,256,320,etc.)')
        print ('')
        print ('       Database Summaries:')
        print ('                    summary     all         (total albums, artists, records)')
        print ('                    summary     artist      (total albums per artist)')
        print ('                    summary     genre       (total records per genre)')
        print ('                    summary     group       (total records per group)')
        print ('                    summary     year        (total records per year)')
        print ('                    summary     bitrate     (total records per bitrate range)')
        print ('')
        print ('       Music list to export to other applications:')
        print ('                    m3u         "artist" "album" "title" "year"')
        print ('')
        print ('           Examples:')
        print ('                    ./tags.py m3u "james taylor" "greatest hits" "" "1976" | mpv --playlist=-')
        print ('')
        print ('                    mpv --playlist <(./tags.py m3u "james taylor" "greatest hits" "" "1976")')
        print ('')
        print ('       Notes:')
        print ('                    current "groups"    (artist,christmas,classical')
        print ('                                          ,compilation,lounge,soundtrack)')
        print ('')
        print ('')


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print ('')
        print (sys.argv[0], ', version ', version)
        MYinfo()
        print ('')
        print ('Usage: ', sys.argv[0], ' [ summary | search | update | m3u | db-build ] {argument} {query}')
        print ('')
    else:
        if sys.argv[1] in ("help","--help","-h"):
            help()
        else:
            script = Script()
            if sys.argv[1] == 'db-build':
                if len(sys.argv) < 3:
                    print (' Must enter a path to your music. ')
                else:
                    script.build(sys.argv[2])
            elif sys.argv[1] == 'update':
                if len(sys.argv) < 3:
                    print (' Must enter a path you are wanting to update. ')
                else:
                    script.update(sys.argv[2])
            elif sys.argv[1] == 'summary':
                if len(sys.argv) < 3:
                    print (' Question: Which summary are you looking for? ')
                    print ('   [ all | artist | genre | group | year | bitrate ] ')
                else:
                    script.summary(sys.argv[2])
            elif sys.argv[1] == 'search':
                if len(sys.argv) < 3:
                    print (' Question: Which search are you looking for? ')
                    print ('   [ artist | album | title | genre | discog | list | bitrate | below320 ] ')
                else:
                    if len(sys.argv) < 4:
                        print (' Question: Which', sys.argv[2], 'are you looking for?')
                    else:
                        script.search(sys.argv[2],sys.argv[3])
            elif sys.argv[1] == 'm3u':
                if len(sys.argv) < 6:
                    arg5 = ''
                else:
                    arg5 = sys.argv[5]
                if len(sys.argv) < 5:
                    arg4 = ''
                else:
                    arg4 = sys.argv[4]
                if len(sys.argv) < 4:
                    arg3 = ''
                else:
                    arg3 = sys.argv[3]
                if len(sys.argv) < 3:
                    print (' M3U needs the following format: "artist" "album" "title" "year" ')
                else:
                    arg2 = sys.argv[2]
                    script.m3u(arg2,arg3,arg4,arg5)
            else:
                print (' Unknown command.')


