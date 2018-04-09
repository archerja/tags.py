tags.py
=======

Latest version = 0.7.0

This python script will create a sqlite database of local music and allow very simple queries.

It is used mainly on Linux, but should work on other OSes.

**Mutagen is required to read mp3 files**

Mutagen is needed to read local mp3 tag information. After initial database creation, it is not needed.

Examples
=======

```
$ ./tags070.py 

./tags070.py , version  0.7
--------------------
database path:  /home/archerja/projects/tags.py/id3.db3
   music path:  /media/archerja/Stuff/backup/Music
--------------------

Usage:  ./tags070.py  {command}   {data}
                    db-build    [your music root path]
                                (only use first time, will delete all records)

                    test        [music path to update]
                                (make sure...)

                    update      [music path to update]
                                (updates the database)

                    not320      [music path to search]
                                (checks database for records below 320 bitrate)

       Database Searches: (using "like")
                    artist      "string"
                    album       "string"
                    title       "string"
                    genre       "string"

       Database Summaries:
                    summary     all
                    summary     genre
                    summary     bitrate
                    summary     group

```



Author
======

Joseph Archer (C) 2015


License
=======

The code is covered by the MIT.
