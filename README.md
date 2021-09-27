# tags.py

This python script will create an sqlite database of local music and allow very simple queries.

It is used mainly on Linux, but should work on other OSes.

## Installation

This script requires [mutagen](https://github.com/quodlibet/mutagen) to pull the mp3 tags out of your files.

Mutagen is needed to read local mp3 tag information that is inserted into the database.

## Usage examples

```
$ ./tags.py 

./tags.py , version  0.8.1
--------------------
database path:  /media/archerja/Extreme SSD/bin/id3.db3
   music path:  /media/archerja/Extreme SSD/Music
--------------------

Usage:  ./tags.py  [ help | summary | search | update | m3u | db-build ] {argument} {query}

```

```
$ ./tags.py summary
 Question: Which summary are you looking for? 
   [ all | artist | genre | group | year | bitrate ] 

```

```
$ ./tags.py search
 Question: Which search are you looking for? 
   [ artist | album | title | year | genre | discog | group | bitrate | below320 ] 
$ ./tags.py search artist
 Question: Which artist are you looking for?
$ ./tags.py search artist "Heart"

```

## Help

```
$ ./tags.py --help

./tags.py , version  0.8.1
--------------------
database path:  /media/archerja/Extreme SSD/bin/id3.db3
   music path:  /media/archerja/Extreme SSD/Music
--------------------

Usage:  ./tags.py  [ summary | search | update | m3u | db-build ] {argument} {query}

                    db-build    [your music root path]
                                (only use first time, will delete all records)

                    update      [music path to update]
                                (updates the database)

       Database Searches:
                    search      artist      "string" (using "like")
                    search      album       "string" (using "like")
                    search      title       "string" (using "like")
                    search      year        "string" (using "like")
                    search      genre       "string" (using "like")
                    search      discog      "string" (using "like", for artist)
                    search      group       "string" (using "like", for groups)
                    search      below320    "group"  (using "like")
                    search      bitrate     "string" (128,256,320,etc.)

       Database Summaries:
                    summary     all         (total albums, artists, records)
                    summary     artist      (total albums per artist)
                    summary     genre       (total records per genre)
                    summary     group       (total records per group)
                    summary     year        (total records per year)
                    summary     bitrate     (total records per bitrate range)

       Music list to export to other applications:
                    m3u         "artist" "album" "title" "year"

           Examples:
                    ./tags.py m3u "james taylor" "greatest hits" "" "1976" | mpv --playlist=-

                    mpv --playlist <(./tags.py m3u "james taylor" "greatest hits" "" "1976")

       Notes:
                    current "groups"    (artist,christmas,classical
                                          ,compilation,lounge,soundtrack)

```

## Release History

* 0.8.1
    * Show error if db and music paths differ
    * Added year search
* 0.8.0
    * Rewrite and cleanup
    * Added m3u search
* 0.7.7
    * Added list search
    * More work on help section
* 0.7.6
    * Added discog search
    * Worked on help section
* 0.7.5
    * Added bitrate searches
* 0.7.0
    * Added several summary queries
    * Added genre search
* 0.3.0
    * The first proper release
    * Added simple searches
* 0.0.1
    * Work in progress



## Author

Joseph Archer (C) 2017


## License

The code is covered by the MIT.
