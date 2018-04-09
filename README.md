tags.py
=======

Latest version = 0.7.7

This python script will create a sqlite database of local music and allow very simple queries.

It is used mainly on Linux, but should work on other OSes.

**Mutagen is required to read mp3 files**

Mutagen is needed to read local mp3 tag information. After initial database creation, it is not needed.

Examples
=======

```
$ ./tags.py 

./tags.py , version  0.7.7
--------------------
database path:  /home/archerja/projects/tags.py/id3.db3
   music path:  /media/archerja/Stuff/backup/Music
--------------------

Usage:  ./tags.py  {command}   {data}
                    db-build    [your music root path]
                                (only use first time, will delete all records)

                    test        [music path to update]
                                (make sure...)

                    update      [music path to update]
                                (updates the database)

       Database Searches:
                    artist      "string" (using "like")
                    album       "string" (using "like")
                    title       "string" (using "like")
                    genre       "string" (using "like")
                    discog      "string" (using "like", for artist)
                    list        "group"  (using "like")
                    below320    "group"  (using "like")
                    bitrate     "string" (128,256,320,etc.)

       Database Summaries:
                    summary     all     (total albums, artists, records)
                    summary     genre   (total records per genre)
                    summary     bitrate (total records per bitrate range)
                    summary     group   (total records per group)
                    summary     artist  (total albums per artist)

       Notes:
                    current "groups"    (artist,christmas,classical
                                          ,compilation,lounge,soundtrack)

```



Author
======

Joseph Archer (C) 2017


License
=======

The code is covered by the MIT.
