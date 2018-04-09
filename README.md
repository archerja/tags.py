tags.py
=======

Latest version = 0.7.5

This python script will create a sqlite database of local music and allow very simple queries.

It is used mainly on Linux, but should work on other OSes.

**Mutagen is required to read mp3 files**

Mutagen is needed to read local mp3 tag information. After initial database creation, it is not needed.

Examples
=======

```
$ ./tags.py 

./tags.py , version  0.7.5
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
                    bitrate     "string" 
                    below320    "group"

       Database Summaries:
                    summary     all
                    summary     genre
                    summary     bitrate
                    summary     group
                    summary     artist

```



Author
======

Joseph Archer (C) 2016


License
=======

The code is covered by the MIT.
